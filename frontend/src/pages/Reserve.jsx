import React, {useEffect, useState} from 'react'

export default function Reserve({bikeId}){
  const [bike, setBike] = useState(null)
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState(null)

  useEffect(()=>{
    if(!bikeId) return
    fetch('/api/bikes')
      .then(r=>r.json())
      .then(list=> setBike(list.find(b=> String(b.id) === String(bikeId))))
      .catch(err=> console.error(err))
  },[bikeId])

  function submit(e){
    e.preventDefault()
    setMessage(null)
    if(!start || !end){ setMessage('Veuillez renseigner les deux dates'); return }
    if(new Date(start) >= new Date(end)){ setMessage('La date de fin doit être après la date de début'); return }
    setLoading(true)
    fetch('/api/reservations', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ bike_id: bike.id, start: start, end: end })
    }).then(async r=>{
      setLoading(false)
      const j = await r.json().catch(()=> null)
      if(r.ok) return j
      throw j || { error: 'Erreur' }
    }).then(data=>{
      setMessage('Réservation créée avec succès')
    }).catch(err=>{
      setMessage('Erreur: ' + (err.error || err.message || 'erreur'))
    })
  }

  if(!bikeId) return <div>Vélo non sélectionné</div>
  if(!bike) return <div>Chargement du vélo...</div>

  // price estimate helper
  const estimate = (()=>{
    if(!start || !end) return null
    const s = new Date(start)
    const e = new Date(end)
    if(isNaN(s) || isNaN(e) || e<=s) return null
    const hours = Math.ceil((e - s) / (1000*60*60))
    return { hours, total: hours * bike.price_per_hour }
  })()

  return (
    <section style={{maxWidth:900, margin:'20px auto'}}>
      <div style={{display:'flex', gap:24, alignItems:'flex-start'}}>
        <img src={bike.image_url} alt={bike.name} style={{width:360, height:260, objectFit:'cover', borderRadius:12}} />
        <div style={{flex:1}}>
          <h2>{bike.name}</h2>
          <p style={{color:'#444'}}>{bike.description}</p>
          <p className="price">{bike.price_per_hour} {bike.currency}/heure</p>

          <form onSubmit={submit} style={{marginTop:20, display:'grid', gap:12}}>
            <div className="form-group">
              <label>Début</label>
              <input className="form-control" type="datetime-local" value={start} onChange={e=>setStart(e.target.value)} />
            </div>
            <div className="form-group">
              <label>Fin</label>
              <input className="form-control" type="datetime-local" value={end} onChange={e=>setEnd(e.target.value)} />
            </div>
            {estimate && <div style={{padding:12, background:'#fff7f7', borderRadius:8}}>Estimation: {estimate.hours}h — <strong>{estimate.total} {bike.currency}</strong></div>}
            <div>
              <button className="btn" type="submit" disabled={loading}>{loading? 'Réservation...' : 'Réserver'}</button>
            </div>
            {message && <div style={{marginTop:12}} className="flash">{message}</div>}
          </form>
        </div>
      </div>
    </section>
  )
}
