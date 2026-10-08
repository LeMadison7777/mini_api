import React, {useEffect, useState} from 'react'

export default function Header(){
  const [me, setMe] = useState({authenticated:false})
  const [q, setQ] = useState('')
  useEffect(()=>{
    fetch('/api/me', {credentials:'include'})
      .then(r=>r.json()).then(setMe).catch(()=>{})
  },[])
  return (
    <header style={{padding:16, borderBottom:'1px solid #eee', background:'#fff'}}>
      <div style={{maxWidth:1100, margin:'0 auto', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <div style={{display:'flex', gap:12, alignItems:'center'}}>
          <div style={{width:44, height:44, background:'linear-gradient(135deg,#ff8a80,#ff5a5f)', borderRadius:8}}></div>
          <a href="#/" style={{fontWeight:700, fontSize:18, color:'#222'}}>BikeRental</a>
          <div style={{marginLeft:16}}>
            <input value={q} onChange={e=> setQ(e.target.value)} placeholder="Chercher un vélo, ex: VTT" style={{padding:'6px 10px', borderRadius:8, border:'1px solid #e7e7e7', width:260}} />
            <button className="btn" style={{marginLeft:8}} onClick={()=> window.location.hash = '#/?q=' + encodeURIComponent(q)}>Rechercher</button>
          </div>
        </div>
        <nav>
          <a href="#/" style={{marginRight:12}}>Home</a>
          <a href="#/about" style={{marginRight:12}}>About</a>
          {me.authenticated ? (
            <>
              <a href="#/dashboard" style={{marginRight:12}}>{me.username}</a>
            </>
          ) : (
            <>
              <a href="#/login" style={{marginRight:12}}>Se connecter</a>
              <a href="#/register">S'inscrire</a>
            </>
          )}
          <span style={{marginLeft:12}}><img src="/static/img/avatar-placeholder.svg" alt="avatar" style={{width:36,height:36,borderRadius:8}}/></span>
        </nav>
      </div>
    </header>
  )
}
