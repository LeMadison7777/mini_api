import React, {useState, useEffect} from 'react'
import Home from './pages/Home'
import About from './pages/About'
import Reserve from './pages/Reserve'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'

export default function App(){
  const [route, setRoute] = useState(window.location.hash.slice(1) || '/')

  useEffect(()=>{
    const onHash = ()=> setRoute(window.location.hash.slice(1) || '/')
    window.addEventListener('hashchange', onHash)
    return ()=> window.removeEventListener('hashchange', onHash)
  },[])

  const render = () => {
    if(route.startsWith('/reserve')){
      const parts = route.split('/')
      const id = parts[2]
      return <Reserve bikeId={id} />
    }
  if(route === '/about') return <About />
  if(route === '/login') return <Login />
  if(route === '/register') return <Register />
  if(route === '/dashboard') return <Dashboard />
  return <Home />
  }

  return (
    <div>
      <nav style={{padding:12, background:'#fff', borderBottom:'1px solid #eee'}}>
        <a href="#/">Home</a>
        <span style={{margin:'0 8px'}}>|</span>
        <a href="#/about">About</a>
      </nav>
      <main style={{padding:20}}>
        {render()}
      </main>
    </div>
  )
}
