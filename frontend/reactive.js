// code based on:
// https://dev.to/ryansolid/a-hands-on-introduction-to-fine-grained-reactivity-3ndf
// https://dev.to/ryansolid/building-a-reactive-library-from-scratch-1i0p


const context = [];

class Effect {
    constructor(fn) {
        this.fn = fn;
        this.assoicatedSignals = new Set();
        this.isStale = false;
        this.memoSignalRef = undefined;
        this.execute();
    }

    cleanup() {
        for (const signal of this.assoicatedSignals) {
            signal.removeEffect(this);
        }    
        this.assoicatedSignals = new Set();
    }

    execute() {
        this.cleanup();
        context.push(this);
        try {
            this.fn();
        }
        finally {
            context.pop();
        }
    }
}

class Signal {
    constructor(value) {
        this.value = value;
        this.associatedEffects = new Set();
        this.memoEffectRef = undefined;
    }

    get() {
        if (context.length > 0) {
            const runningEffect = context[context.length - 1];
            this.associatedEffects.add(runningEffect);
            runningEffect.assoicatedSignals.add(this);
            if (this.memoEffectRef && this.memoEffectRef.isStale) {
                this.memoEffectRef.isStale = false;
                this.memoEffectRef.execute();
            }
        }
        return this.value;
    }

    _set(value) {
        this.value = value; 
        for (const effect of this.associatedEffects) {
            if (!effect.isStale) continue;
            effect.isStale = false;
            effect.execute();
        }
    }

    set(value) {
        this.propagateStale();
        this._set(value);
    }

    propagateStale() {
        for (const effect of this.associatedEffects) {
            if (!effect.isStale) {
                effect.isStale = true;
                if (effect.memoSignalRef) {
                    effect.memoSignalRef.propagateStale();
                }
            }
        }
    }

    removeEffect(effect) {
        if (this.associatedEffects.has(effect)) {
            this.associatedEffects.delete(effect);
        }
    }
}

function createSignal(value) {
    const signal = new Signal(value);
    return [() => signal.get(), (value) => signal.set(value)];
}

function createEffect(fn) {
    return new Effect(fn);
}

function createMemo(fn) {
    const signal = new Signal();
    const effect = new Effect(() => signal._set(fn()));
    signal.memoEffectRef = effect;
    effect.memoSignalRef = signal;
    return () => signal.get();
}

export { createSignal, createEffect, createMemo };