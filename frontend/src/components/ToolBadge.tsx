interface ToolBadgeProps {
  toolName: string | null;
}

export default function ToolBadge({ toolName }: ToolBadgeProps) {
  if (!toolName) {
    return null;
  }

  return <div className="tool-badge">Tool: {toolName}</div>;
}
