/**
 * React wrapper around react-joyride v3 used by the `reflex-react-joyride`
 * custom component.
 *
 * Responsibilities:
 * - Drive the tour through the `useJoyride` hook, so the `controls` object is
 *   available for the imperative Python helpers in `actions.py`
 *   (`window.__reflexJoyride[tourId]`).
 * - Normalize `snake_case` keys coming from Python into the `camelCase` keys
 *   react-joyride expects, for steps, options, locale, styles and floating
 *   options alike. The conversion is idempotent, so `camelCase` input (and
 *   anything already normalized on the Python side) passes through untouched.
 * - Reduce react-joyride's event payload, which carries React nodes and
 *   functions, to a flat JSON-safe object the Reflex backend can receive, and
 *   fan it out to the catch-all `onEvent` plus the per-event triggers.
 * - Adapt the optional `tooltip` and `beacon` render props into stable React
 *   components so custom tooltips do not remount on every render.
 */
import { useEffect, useRef } from "react";
import { useJoyride } from "react-joyride";

const REGISTRY_KEY = "__reflexJoyride";

/** Keys whose values are passed through verbatim (user payload, React nodes). */
const OPAQUE_KEYS = new Set(["data", "content", "title"]);

const isPlainObject = (value) =>
  value !== null &&
  typeof value === "object" &&
  (value.constructor === Object || value.constructor === undefined) &&
  value.$$typeof === undefined &&
  !(typeof Element !== "undefined" && value instanceof Element);

/** spotlight_padding -> spotlightPadding; leaves _hover, --var and camelCase alone. */
const toCamelKey = (key) => {
  if (typeof key !== "string" || key.startsWith("_") || key.startsWith("-") || !key.includes("_")) {
    return key;
  }
  return key.replace(/_+([a-zA-Z0-9])/g, (_match, char) => char.toUpperCase());
};

/** Recursively camelCase the keys of plain objects and arrays. */
const camelize = (value) => {
  if (Array.isArray(value)) return value.map(camelize);
  if (!isPlainObject(value)) return value;

  const out = {};
  for (const [key, item] of Object.entries(value)) {
    out[toCamelKey(key)] = OPAQUE_KEYS.has(key) ? item : camelize(item);
  }
  return out;
};

/**
 * A cheap identity key for a prop, used to avoid rebuilding (and thereby
 * resetting) the normalized value on every render. Falls back to a unique
 * marker when the value cannot be stringified, so correctness never depends
 * on the fast path.
 */
let uncacheable = 0;
const stableKey = (value) => {
  if (value === undefined || value === null) return "~null";
  const seen = new WeakSet();
  try {
    return JSON.stringify(value, (_key, item) => {
      if (typeof item === "function") return "~fn";
      if (item !== null && typeof item === "object") {
        if (seen.has(item)) return "~circular";
        seen.add(item);
      }
      return item;
    });
  } catch {
    uncacheable += 1;
    return "~uncacheable:" + uncacheable;
  }
};

/** Memoize camelize(value) by content rather than by object identity. */
const useNormalized = (value) => {
  const cache = useRef({ key: undefined, value: undefined });
  const key = stableKey(value);
  if (key !== cache.current.key) {
    cache.current = { key, value: value === undefined || value === null ? value : camelize(value) };
  }
  return cache.current.value;
};

/** A ref that always holds the latest render's value. */
const useLatest = (value) => {
  const ref = useRef(value);
  ref.current = value;
  return ref;
};

const asString = (value) => (typeof value === "string" ? value : null);

/** Flatten react-joyride's event payload into something JSON-serializable. */
const serializeEvent = (data) => {
  const step = data?.step ?? {};
  const index = typeof data?.index === "number" ? data.index : 0;
  const size = typeof data?.size === "number" ? data.size : 0;

  return {
    type: data?.type ?? null,
    action: data?.action ?? null,
    index,
    size,
    status: data?.status ?? null,
    lifecycle: data?.lifecycle ?? null,
    origin: data?.origin ?? null,
    controlled: Boolean(data?.controlled),
    waiting: Boolean(data?.waiting),
    scrolling: Boolean(data?.scrolling),
    is_last_step: size > 0 && index === size - 1,
    step_id: step.id ?? null,
    step_target: asString(step.target),
    step_title: asString(step.title),
    step_data: step.data ?? null,
    error: data?.error ? String(data.error.message ?? data.error) : null,
  };
};

/** The subset of the tour state returned by the info() action. */
const serializeState = (state) =>
  state
    ? {
        action: state.action ?? null,
        controlled: Boolean(state.controlled),
        index: state.index ?? 0,
        lifecycle: state.lifecycle ?? null,
        origin: state.origin ?? null,
        scrolling: Boolean(state.scrolling),
        size: state.size ?? 0,
        status: state.status ?? null,
        waiting: Boolean(state.waiting),
      }
    : null;

/** Map an event type to the name of its dedicated trigger. */
const TRIGGER_BY_EVENT = {
  "tour:start": "onTourStart",
  "tour:end": "onTourEnd",
  "tour:status": "onStatusChange",
  "step:before": "onStepBefore",
  "step:after": "onStepAfter",
  "scroll:start": "onScrollStart",
  "scroll:end": "onScrollEnd",
  beacon: "onBeacon",
  tooltip: "onTooltip",
  "error:target_not_found": "onTargetNotFound",
  error: "onError",
};

export function JoyrideTour(props) {
  const {
    tourId,
    steps,
    run,
    continuous,
    debug,
    initialStepIndex,
    stepIndex,
    scrollToFirstStep,
    nonce,
    portalElement,
    options,
    locale,
    styles,
    floatingOptions,
    tooltip,
    beacon,
    ...handlers
  } = props;

  const normalizedSteps = useNormalized(steps) ?? [];
  const normalizedOptions = useNormalized(options);
  const normalizedLocale = useNormalized(locale);
  const normalizedStyles = useNormalized(styles);
  const normalizedFloating = useNormalized(floatingOptions);

  const handlersRef = useLatest(handlers);
  const controlsRef = useRef(null);

  // Stable adapters: react-joyride compares component identity, so building the
  // wrapper once and reading the render function from a ref keeps custom
  // tooltips from remounting (and losing focus) on every state update.
  const tooltipRef = useLatest(tooltip);
  const beaconRef = useLatest(beacon);

  const tooltipComponent = useRef(function JoyrideTooltip(tooltipProps) {
    const render = tooltipRef.current;
    if (!render) return null;
    const { step = {}, index = 0, size = 0 } = tooltipProps;

    return (
      <div {...tooltipProps.tooltipProps}>
        {render({
          ...tooltipProps,
          content: step.content ?? null,
          title: step.title ?? null,
          stepId: step.id ?? null,
          stepData: step.data ?? null,
          current: index + 1,
          total: size,
          progress: size ? index + 1 + " / " + size : "",
          isFirstStep: index === 0,
        })}
      </div>
    );
  }).current;

  const beaconComponent = useRef(function JoyrideBeacon(beaconProps) {
    const render = beaconRef.current;
    return render ? <span>{render(beaconProps)}</span> : null;
  }).current;

  const config = {
    steps: normalizedSteps,
    continuous: Boolean(continuous),
    debug: Boolean(debug),
    run: Boolean(run),
    scrollToFirstStep: Boolean(scrollToFirstStep),
    onEvent: (data, controls) => {
      controlsRef.current = controls;
      const payload = serializeEvent(data);
      const current = handlersRef.current;

      current.onEvent?.(payload);
      const trigger = TRIGGER_BY_EVENT[payload.type];
      if (trigger) current[trigger]?.(payload);
    },
  };

  if (typeof initialStepIndex === "number") config.initialStepIndex = initialStepIndex;
  if (typeof stepIndex === "number") config.stepIndex = stepIndex;
  if (nonce) config.nonce = nonce;
  if (portalElement) config.portalElement = portalElement;
  if (normalizedOptions) config.options = normalizedOptions;
  if (normalizedLocale) config.locale = normalizedLocale;
  if (normalizedStyles) config.styles = normalizedStyles;
  if (normalizedFloating) config.floatingOptions = normalizedFloating;
  if (tooltip) config.tooltipComponent = tooltipComponent;
  if (beacon) config.beaconComponent = beaconComponent;

  const { controls, Tour } = useJoyride(config);
  controlsRef.current = controls;

  // Publish the imperative API used by the Python action helpers.
  useEffect(() => {
    if (!tourId || typeof window === "undefined") return undefined;

    const registry = (window[REGISTRY_KEY] = window[REGISTRY_KEY] || {});
    const api = {
      start: (index) => controlsRef.current?.start(index),
      stop: (advance) => controlsRef.current?.stop(advance),
      next: () => controlsRef.current?.next(),
      prev: () => controlsRef.current?.prev(),
      go: (index) => controlsRef.current?.go(index),
      close: () => controlsRef.current?.close(),
      skip: () => controlsRef.current?.skip(),
      reset: (restart) => controlsRef.current?.reset(restart),
      replay: () => controlsRef.current?.replay(),
      open: () => controlsRef.current?.open(),
      info: () => serializeState(controlsRef.current?.info()),
    };

    registry[tourId] = api;
    return () => {
      if (registry[tourId] === api) delete registry[tourId];
    };
  }, [tourId]);

  return Tour;
}

export default JoyrideTour;
