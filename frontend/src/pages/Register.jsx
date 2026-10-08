import React, {useState} from 'react'

export default function Register(){
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState(null)

  function submit(e){
    e.preventDefault()
    fetch('/api/register', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username,email,password})})
      .then(async r=>{
        if(r.ok) return r.json()
        const j = await r.json().catch(()=>({error:'unknown'}))
        throw j
      }).then(()=>{ window.location.hash = '#/login' })
      .catch(err=> setMsg(err.error || 'Erreur'))
  }

  return (
    <section style={{maxWidth:480, margin:'20px auto'}}>
      <h2>Inscription</h2>
      <form onSubmit={submit} style={{display:'grid', gap:12}}>
        <input className="form-control" placeholder="Nom d'utilisateur" value={username} onChange={e=>setUsername(e.target.value)} />
        <input className="form-control" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="form-control" type="password" placeholder="Mot de passe" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="btn">S'inscrire</button>
        {msg && <div className="flash">{msg}</div>}
      </form>
    </section>
  )
}
