import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App'
import Header from './components/Header'
import './styles.css'

createRoot(document.getElementById('root')).render(
	<>
		<Header />
		<App />
	</>
)
