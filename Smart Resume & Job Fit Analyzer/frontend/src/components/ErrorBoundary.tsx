import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
    children?: ReactNode;
    fallback?: ReactNode;
}

interface State {
    hasError: boolean;
    error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
    public state: State = {
        hasError: false,
        error: null,
    };

    public static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Uncaught error:', error, errorInfo);
    }

    private handleReload = () => {
        window.location.reload();
    };

    private handleHome = () => {
        window.location.href = '/';
    };

    public render() {
        if (this.state.hasError) {
            if (this.props.fallback) {
                return this.props.fallback;
            }

            return (
                <div className="min-h-screen flex items-center justify-center bg-[var(--color-neutral-50)] p-4">
                    <div className="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center animate-fade-in border border-[var(--color-neutral-200)]">
                        <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                            <AlertTriangle className="w-8 h-8 text-red-600" />
                        </div>

                        <h2 className="text-2xl font-bold text-[var(--color-neutral-900)] mb-2">
                            Something went wrong
                        </h2>

                        <p className="text-[var(--color-neutral-500)] mb-6">
                            We encountered an unexpected error. Don't worry, your data is safe.
                        </p>

                        {this.state.error && (
                            <div className="bg-[var(--color-neutral-50)] p-4 rounded-lg mb-6 text-left overflow-auto max-h-32 text-xs text-[var(--color-neutral-600)] font-mono border border-[var(--color-neutral-200)]">
                                {this.state.error.toString()}
                            </div>
                        )}

                        <div className="flex flex-col gap-3">
                            <button
                                onClick={this.handleReload}
                                className="w-full btn btn-primary flex items-center justify-center gap-2 py-3"
                            >
                                <RefreshCw className="w-4 h-4" />
                                Reload Page
                            </button>

                            <button
                                onClick={this.handleHome}
                                className="w-full btn btn-secondary flex items-center justify-center gap-2 py-3"
                            >
                                <Home className="w-4 h-4" />
                                Go to Home
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
