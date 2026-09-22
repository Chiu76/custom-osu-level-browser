const context = [];

function subscribe(running_subscriber, subscriptions) {
    subscriptions.add(running_subscriber);
    running_subscriber.dependencies.add(subscriptions);
}

export function createSignal(value) {
    const subscriptions = new Set();

    const read = () => {
        const running_subscriber = context[context.length - 1];
        if (running_subscriber) subscribe(running_subscriber, subscriptions);
        return value;
    };

    const write = (nextValue) => {
        value = nextValue;
        for (const sub of [...subscriptions]) {
            sub.execute()
        }
    };

    return [read, write];
};

export function createEffect(fn) {
    const cleanup = () => {
        for (const dep of running_subscriber.dependencies) dep.delete(running_subscriber);
        running_subscriber.dependencies.clear();
    }

    const execute = () => {
        cleanup()
        context.push(running_subscriber);
        try {
            fn();
        } finally {
            context.pop();
        }
    };

    const running_subscriber = {
        execute,
        dependencies: new Set()
    };

    execute();
}

export function createMemo(fn) {
    const [s, set] = createSignal();
    createEffect(() => set(fn()));
    return s;
}