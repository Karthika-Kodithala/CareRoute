# Integration Contract

## API
`POST /api/chat`

Request:
```json
{
  "session_id": "demo-001",
  "message": "I'm dizzy."
}
```

Response must follow `backend/app/models/schemas.py`.

## P1 → P2
P1 supplies structured patient context and navigation query.

P2 returns:
- grounded context;
- sources;
- verification result.

## P1 → P3
P1 emits evaluation traces after each evaluated turn.

## P3 → P4
P3 supplies:
- V1 metrics;
- V2 metrics;
- failure description;
- engineering fix;
- measured delta.

## P4
Never hard-code final PRISM numbers. Read the recorded results supplied by P3.

## Integration sequence
1. P1 gets `/api/chat` working with mock data.
2. P4 connects to the mock contract.
3. P2 plugs retrieval/safety into P1.
4. P3 consumes traces and runs V1.
5. Freeze V1.
6. PRISM identifies a real weakness.
7. P1/P2 implement the targeted fix.
8. Run the identical scenario set for V2.
9. P3 records before/after evidence.
10. P4 replaces placeholders with actual evidence.
