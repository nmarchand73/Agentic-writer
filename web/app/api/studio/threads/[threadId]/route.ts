import { NextResponse } from "next/server";
import { studioRunner } from "@/lib/studio-runtime";

export async function DELETE(
  _request: Request,
  { params }: { params: Promise<{ threadId: string }> },
) {
  const { threadId } = await params;
  if (!threadId) {
    return NextResponse.json({ error: "threadId required" }, { status: 400 });
  }
  studioRunner.deleteThread(threadId);
  return NextResponse.json({ threadId, deleted: true });
}
