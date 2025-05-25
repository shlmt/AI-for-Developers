const express = require('express')
const cors = require('cors')
const { OpenAI } = require('openai')
require("dotenv").config()

const PORT = process.env.PORT || 1111

const app = express()
app.use(cors())
app.use(express.json())

if (!process.env.API_KEY) {
	throw new Error('Missing API key')
}

const openaiClient = new OpenAI({
	apiKey: process.env.API_KEY
})

const history = {}

app.post('/', async (req, res) => {
	const { prompt } = req.body
	const userId = req.headers.authorization?.split(' ')[1]
    if (!prompt) {
		return res.status(404).json({ msg: 'Missing prompt' })
	}
	if (!userId) {
		return res.status(401).json({ msg: 'Missing or invalid authorization header' })
	}

	history[userId] ??= []
	history[userId].push({ role: 'user', content: prompt })
	const messages = [{ role: 'system', content: 'Talk like a pirate.' }, ...history[userId]]

	try {
		const completion = await openaiClient.chat.completions.create({
			model: 'gpt-4o',
			messages
		})
		const answer = completion.choices[0].message.content
		history[userId].push({ role: 'assistant', content: answer })
		res.json({ msg: answer })
	}
    catch (err) {
		console.log(err)
		res.status(400).json({ msg: 'error' })
	}
})

app.listen(PORT, () => {
	console.log(`server running on port: ${PORT}`)
})
