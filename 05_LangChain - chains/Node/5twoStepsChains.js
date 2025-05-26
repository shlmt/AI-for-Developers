import { StringOutputParser } from '@langchain/core/output_parsers'
import { ChatPromptTemplate, PromptTemplate } from '@langchain/core/prompts'
import { RunnableLambda, RunnableSequence } from '@langchain/core/runnables'
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

const nameTemplate = ChatPromptTemplate.fromMessages([
	{
		role: 'system',
		content:
			'You are an expert copywriter and advertiser. Answer only one answer to what was asked of you without adding comments or questions or simbols.'
	},
	{
		role: 'user',
		content: 'I want to open a fancy restaurant for {cuisine} food. Sugget a fancy name for this.'
	}
])

const nameChain = nameTemplate.pipe(llm).pipe(new StringOutputParser())

const foodTemplate = PromptTemplate.fromTemplate(
	'Suggest some menu items for {restaurant_name}. Return it as a comma seperated list'
)

const foodChain = foodTemplate.pipe(llm).pipe(new StringOutputParser())

// // compose simply
const composedChain = RunnableSequence.from([nameChain, (res) => ({ restaurant_name: res }), foodChain])
const res = await composedChain.invoke({ cuisine: 'greec'})

console.log(res)

// compose & recieve the outputs of two chains
const composedChain2Ans = new RunnableLambda({
	func: async ({ cuisine }) => {
		const restaurant_name = await nameChain.invoke({ cuisine })
		const menu_items = await foodChain.invoke({ restaurant_name })
		return { restaurant_name, menu_items }
	}
})

const res2 = await composedChain2Ans.invoke({ cuisine: 'israely' })

console.log(res2)

