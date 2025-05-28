import { DynamicStructuredTool } from '@langchain/core/tools'
import { ChatGroq } from '@langchain/groq'
import { Annotation, END, START, messagesStateReducer, StateGraph } from '@langchain/langgraph'
import { ToolNode, toolsCondition } from '@langchain/langgraph/prebuilt'
import { HumanMessage, SystemMessage } from '@langchain/core/messages'
import { z } from 'zod'
import dotenv from 'dotenv'
dotenv.config()

const rateTool = new DynamicStructuredTool({
	name: 'getExchangeRate',
	description: 'Get the latest exchange rates from a given base currency to symbol.',
	schema: z.object({
		base: z.string().describe('The base currency like USD'),
		symbol: z.string().describe('The target currency like ILS')
	}),
	func: async ({ base, symbol }) => {
		if (!base || !symbol) {
			return 'Base currency and symbol are required'
		}
		if (typeof base != 'string' || typeof symbol != 'string') {
			return 'Base currency and symbol must be strings'
		}
		// refactor to use params object
		const params = new URLSearchParams({
			base: base.toUpperCase(),
			symbols: symbol.toUpperCase(),
			access_key: process.env.EXCHANGERATE_API_KEY
        })
		const req = `https://api.exchangeratesapi.io/v1/latest?${params.toString()}`
		const res = await fetch(req)
		if (!res.ok) {
			return 'Failed to fetch exchange rates'
		}
		const data = await res.json()
		return data.rates[symbol] || null
	}
})

const tools = [rateTool]

const model = new ChatGroq({
	apiKey: process.env.GROQ_API_KEY,
	model: 'llama-3.3-70b-versatile'
}).bindTools(tools)

const state = Annotation.Root({
	messages: Annotation({
		reducer: messagesStateReducer,
		default: () => [
			new SystemMessage(
				'you are a helpful assistant that can answer questions about exchange rates. ' +
					'You can use the getExchangeRate tool to get the latest exchange rates. ' +
					'Finally give a nice answer to the user. '
			)
		]
	})
})

const runLLM = async (state) => {
	const res = await model.invoke(state.messages)
	return {
		messages: res
	}
}

const toolNode = new ToolNode(tools)

const graphBuilder = new StateGraph(state)

graphBuilder.addNode('run llm', runLLM)
graphBuilder.addNode('tools', toolNode)
graphBuilder.addNode('llm nice answer', runLLM)

graphBuilder.addEdge(START, 'run llm')
graphBuilder.addConditionalEdges('run llm', toolsCondition)
graphBuilder.addEdge('tools', 'llm nice answer')
graphBuilder.addEdge('llm nice answer', END)

const graph = graphBuilder.compile()

const res = await graph.invoke({
	messages: [new HumanMessage('how match it 10 euro if I wants indian or south africa coins?')]
})
console.log('Agent response:', res.messages[res.messages.length - 1].content)

