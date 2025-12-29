# LLM Integration Setup Guide

## Quick Start

The app now uses **real Hugging Face LLM** for natural language task parsing!

### Step 1: Get Hugging Face API Token

1. **Sign up** (free): https://huggingface.co/join
2. **Get API token**: https://huggingface.co/settings/tokens
3. **Create a token** (read access is enough)

### Step 2: Add Token to Environment

Add to your `backend/.env` file:

```bash
HF_API_TOKEN=your_token_here
```

### Step 3: Restart Backend

```bash
cd backend
uvicorn main:app --reload
```

### Step 4: Test It!

1. Open the app
2. Click "✨ Try AI Mode" in task form
3. Enter: `"Call dentist next Friday at 2pm"`
4. Click "Parse with AI"
5. Watch the magic! 🎉

---

## How It Works

### With API Token (LLM Mode)

- Uses **Google Flan-T5-Base** model via Hugging Face API
- Sends natural language to LLM with structured prompt
- LLM extracts: title, description, due_date
- Returns structured JSON
- **Higher accuracy** for complex inputs

### Without API Token (Fallback Mode)

- Uses **rule-based parsing** (regex + patterns)
- Works offline, no API needed
- Still functional, just less sophisticated
- **Good enough** for simple inputs

---

## Model Details

**Model**: `google/flan-t5-base`
- **Type**: Instruction-tuned language model
- **Size**: ~250MB (runs on Hugging Face servers)
- **Best for**: Following instructions, structured output
- **Free tier**: Rate limited but works for development

**Why This Model?**
- ✅ Good at instruction following
- ✅ Can extract structured data
- ✅ Fast inference
- ✅ Free tier available
- ✅ No local GPU needed

---

## API Usage

### Free Tier Limits

- **Rate limit**: ~30 requests/minute (approximate)
- **No cost**: Free for reasonable usage
- **Upgrade**: Available if needed (not required for this project)

### Error Handling

The app handles:
- ✅ API timeouts (falls back to rule-based)
- ✅ Rate limits (falls back to rule-based)
- ✅ Network errors (falls back to rule-based)
- ✅ Invalid responses (falls back to rule-based)

**You'll never see an error** - it just uses the fallback!

---

## Testing

### Test with LLM

```bash
# With API token set
curl -X POST http://127.0.0.1:8000/tasks/ai-parse \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Call dentist next Friday at 2pm"}'
```

**Expected response:**
```json
{
  "title": "Call dentist",
  "description": null,
  "due_date": "2024-01-19T14:00:00Z",
  "confidence": 0.85
}
```

### Test without LLM (fallback)

```bash
# Without API token (or if API fails)
# Same request, but uses rule-based parsing
# Still works, just different parsing method
```

---

## Troubleshooting

### "LLM not working"

1. **Check token**: Is `HF_API_TOKEN` in `.env`?
2. **Check format**: Token should be `hf_...` format
3. **Restart server**: Changes to `.env` require restart
4. **Check logs**: Look for API errors in console

### "Getting rate limited"

- Free tier has limits
- Wait a minute and try again
- App automatically falls back to rule-based

### "API timeout"

- Network might be slow
- App automatically falls back
- Try again later

---

## For Internship Review

### What to Say

"I integrated **Hugging Face's Flan-T5-Base LLM** for natural language task parsing. The system uses a hybrid approach:

1. **Primary**: LLM-powered parsing via Hugging Face API
2. **Fallback**: Rule-based parsing if API unavailable

This ensures the feature always works, even without internet or API access. The LLM provides better accuracy for complex inputs like 'Schedule team meeting next Monday at 3pm with agenda discussion'."

### Key Points

- ✅ Real LLM integration (not just rule-based)
- ✅ Production-ready error handling
- ✅ Graceful degradation
- ✅ Free tier friendly
- ✅ No breaking changes

---

## Advanced: Custom Model

Want to use a different model? Edit `backend/ai_parser.py`:

```python
HF_MODEL = "your-model-name-here"
```

**Popular alternatives:**
- `google/flan-t5-large` - More accurate, slower
- `microsoft/DialoGPT-medium` - Conversational
- `facebook/bart-large-cnn` - Summarization

---

## Summary

✅ **Real LLM**: Hugging Face Flan-T5-Base
✅ **Free tier**: Works for development
✅ **Always works**: Falls back gracefully
✅ **Production-ready**: Error handling built-in

**The app now has actual AI!** 🚀

