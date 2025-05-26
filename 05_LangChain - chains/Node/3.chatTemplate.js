import { ChatPromptTemplate, PromptTemplate } from '@langchain/core/prompts'
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

const promptTemplate = ChatPromptTemplate.fromMessages([
	{
		role: 'system',
		content:
			'You are an expert copywriter and advertiser. Answer only one answer to what was asked of you without adding comments or questions.'
	},
	{
		role: 'user',
		content: 'I want to open a fancy restaurant for {cuisine} food. Sugget a fancy name for this.'
	}
])

const prompt = await promptTemplate.invoke({ cuisine: 'italian' })

const answer = await llm.invoke(prompt)

console.log(answer.content)
