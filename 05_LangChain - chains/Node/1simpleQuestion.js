import { ChatGoogleGenerativeAI } from '@langchain/google-genai'
import dotenv from 'dotenv'
dotenv.config()

const API_KEY = process.env.GOOGLE_GENAI_API_KEY

const llm = new ChatGoogleGenerativeAI({
	model: 'gemini-2.0-flash',
	temperature: 0.8,
	maxOutputTokens: 100,
	apiKey: API_KEY
})

const answer = await llm.invoke('Who are you?')
console.log(answer.content)
