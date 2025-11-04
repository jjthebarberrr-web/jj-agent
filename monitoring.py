"""Error monitoring integration (Sentry/OpenTelemetry)."""

import os


class Monitoring:
    """Error monitoring wrapper."""
    
    def __init__(self):
        self.sentry_enabled = os.getenv("JJ_SENTRY_DSN") is not None
        self.otel_enabled = os.getenv("JJ_OTEL_ENDPOINT") is not None
        
        if self.sentry_enabled:
            try:
                import sentry_sdk
                sentry_sdk.init(
                    dsn=os.getenv("JJ_SENTRY_DSN"),
                    environment=os.getenv("JJ_ENV", "development"),
                    traces_sample_rate=0.1,
                )
                self.sentry = sentry_sdk
            except ImportError:
                self.sentry_enabled = False
                self.sentry = None
        else:
            self.sentry = None
        
        if self.otel_enabled:
            try:
                from opentelemetry import trace
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
                from opentelemetry.sdk.trace import TracerProvider
                from opentelemetry.sdk.trace.export import BatchSpanProcessor
                
                provider = TracerProvider()
                processor = BatchSpanProcessor(
                    OTLPSpanExporter(endpoint=os.getenv("JJ_OTEL_ENDPOINT"))
                )
                provider.add_span_processor(processor)
                trace.set_tracer_provider(provider)
                
                self.otel_tracer = trace.get_tracer(__name__)
            except ImportError:
                self.otel_enabled = False
                self.otel_tracer = None
        else:
            self.otel_tracer = None
    
    def capture_exception(self, exception: Exception, **kwargs):
        """Capture exception in monitoring system."""
        if self.sentry_enabled and self.sentry:
            self.sentry.capture_exception(exception, **kwargs)
    
    def start_span(self, name: str, **kwargs):
        """Start OpenTelemetry span."""
        if self.otel_enabled and self.otel_tracer:
            return self.otel_tracer.start_span(name, **kwargs)
        return None


# Global monitoring instance
monitoring = Monitoring()

