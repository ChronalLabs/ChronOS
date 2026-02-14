import express from 'express'
import cors from 'cors'
import dotenv from 'dotenv'
import { GoogleGenerativeAI } from '@google/generative-ai'
// app.use(express.json()) // ✅ Enables JSON body parsing

dotenv.config()

const app = express()
app.use(cors())
app.use(express.json())

app.use((req, res, next) => {
  console.log(`[${req.method}] ${req.url}`)
  next()
})

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY)

app.post('/api/generate-career', async (req, res) => {
  const { userInput } = req.body
  console.log('User input received:', userInput)

  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-flash' })

    const result = await model.generateContent(
      `Suggest a career path for someone who says: "${userInput}"

Return in this format:
Career Title:
Required Skills:
Learning Roadmap:`
    )

    const output = result.response.text()
    res.json({ output })
  } catch (err) {
    console.error('Gemini API error:', err.message)
    res.status(500).json({ error: err.message })
  }
})

const PORT = process.env.PORT || 8000
app.listen(process.env.PORT || 8000, () => {
  console.log(`Server running on port ${process.env.PORT || 8000}`);
});

