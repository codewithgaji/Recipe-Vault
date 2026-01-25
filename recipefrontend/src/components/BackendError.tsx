import { ServerCrash, RefreshCw, Terminal } from "lucide-react";
import { Button } from "@/components/ui/button";

interface BackendErrorProps {
  error: Error;
  onRetry: () => void;
}

export function BackendError({ error, onRetry }: BackendErrorProps) {
  const isConnectionError = error.message.includes("Failed to fetch") ||
    error.message.includes("timed out") ||
    error.message.includes("NetworkError");

  return (
    <div className="flex flex-col items-center justify-center py-20 px-4 text-center animate-fade-in">
      <div className="w-20 h-20 rounded-full bg-destructive/10 flex items-center justify-center mb-6">
        <ServerCrash className="w-10 h-10 text-destructive" />
      </div>
      
      <h2 className="font-display text-2xl font-semibold mb-2">
        {isConnectionError ? "Backend Not Running" : "Connection Error"}
      </h2>
      
      <p className="text-muted-foreground max-w-md mb-6">
        {isConnectionError ? (
          <>
            Can't connect to <code className="bg-muted px-1.5 py-0.5 rounded text-sm font-mono">http://localhost:8000</code>
            <br />
            Make sure your FastAPI server is running.
          </>
        ) : (
          error.message
        )}
      </p>

      {isConnectionError && (
        <div className="bg-muted rounded-lg p-4 mb-6 max-w-lg">
          <div className="flex items-center gap-2 text-sm font-medium mb-2">
            <Terminal className="w-4 h-4" />
            Start your FastAPI backend:
          </div>
          <code className="block text-sm font-mono bg-background/80 rounded p-3 text-left">
            uvicorn main:app --reload
          </code>
        </div>
      )}

      <Button onClick={onRetry} className="gap-2">
        <RefreshCw className="w-4 h-4" />
        Try Again
      </Button>
    </div>
  );
}
