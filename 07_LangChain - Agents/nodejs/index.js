import { ChatGroq } from '@langchain/groq'
import { createToolCallingAgent } from 'langchain/agents'
import { AgentExecutor } from 'langchain/agents'
import { ChatPromptTemplate } from '@langchain/core/prompts'
import { WikipediaQueryRun } from '@langchain/community/tools/wikipedia_query_run'
import getCurrentWeatherTool from './currentWeatherTool.js'
import dotenv from 'dotenv'
dotenv.config()

const model = new ChatGroq({
	apiKey: process.env.GROQ_API_KEY,
	model: 'llama-3.3-70b-versatile'
})

const wikipediaTool = new WikipediaQueryRun({
	topKResults: 1,
	maxDocContentLength: 4000
})

const tools = [wikipediaTool, getCurrentWeatherTool]

const prompt = ChatPromptTemplate.fromMessages([
	['system', 'You are an assistant with access to two tools. when you have an answer return it.'],
	[
		'human',
		'give me the current weather in the capital city of {input}. Also provide a short interesting fact about the city.'
	],
	['placeholder', '{agent_scratchpad}']
])

const agent = createToolCallingAgent({ llm: model, tools: tools, prompt })
const agentExecutor = new AgentExecutor({ agent, tools })

const res = await agentExecutor.invoke({ input: 'Israel' })
console.log(res.output)
