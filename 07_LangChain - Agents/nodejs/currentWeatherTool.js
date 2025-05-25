import { DynamicTool } from '@langchain/core/tools'
import dotenv from 'dotenv'
dotenv.config()

const WEATHER_API_KEY = process.env.WEATHER_API_KEY

const getCurrentWeatherTool = new DynamicTool({
	name: 'get current weather',
	description: 'Returns the current weather for a city,countryCode (e.g. Jerusalem,IL)',
	func: async (location) => {
		const regex = /^[A-Za-z\s]+,[A-Z]{2}$/
		if (!regex.test(location)) return 'Invalid format. Use City,CountryCode (e.g. Jerusalem,IL)'
		const params = new URLSearchParams({
			appid: WEATHER_API_KEY,
			units: 'metric',
			lang: 'en',
			q: location
		})
		const res = await fetch(`https://api.openweathermap.org/data/2.5/weather?${params}`)
		if (res.ok) {
			const data = await res.json()
			return `Temperature: ${data.main.temp}°C, Description: ${data.weather[0].description}`
		} else return 'Error fetching weather data.'
	}
})

export default getCurrentWeatherTool
