import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import z from 'zod'

const server = new McpServer({
	name: 'my-first-mcp',
	version: '1.0.0'
})

server.registerTool(
	'days_until',
	{
		title: 'Days Until Date',
		description: 'Calculates how many days remain until a given future date.',
		inputSchema: {
			year: z.number().int().min(1900),
			month: z.number().int().min(1).max(12),
			day: z.number().int().min(1).max(31)
		}
	},
	async ({ year, month, day }) => {
		const now = new Date()
		const target = new Date(year, month - 1, day)
		const msInDay = 1000 * 60 * 60 * 24
		const diffTime = target.getTime() - now.getTime()
		const daysRemaining = Math.ceil(diffTime / msInDay)

		return {
			content: [
				{
					type: 'number',
					text: daysRemaining
				}
			]
		}
	}
)

server.registerTool(
	'date_after_days',
	{
		title: 'Date After N Days',
		description: 'Calculates the future date after a given number of days from today.',
		inputSchema: {
			daysAhead: z.number().int().min(0).max(3650)
		}
	},
	async ({ daysAhead }) => {
		const now = new Date()
		now.setDate(now.getDate() + daysAhead)
		const fullDate = now.toLocaleDateString('en-US', {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		})

		return {
			content: [
				{
					type: 'text',
					text: fullDate
				}
			]
		}
	}
)

const transport = new StdioServerTransport()
await server.connect(transport)
