import React, {useEffect, useState} from 'react'

export default function Home(){
  const [bikes, setBikes] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('')

  useEffect(()=>{
    // check hash for ?q= query
    const qmatch = window.location.hash.match(/\?q=([^&]+)/)
    if(qmatch) setFilter(decodeURIComponent(qmatch[1]))
    fetch('/api/bikes')
      .then(r=>r.json())
      .then(list=>{ setBikes(list); setLoading(false) })
      .catch(err=>{ console.error(err); setLoading(false) })
  },[])

  return (
    <section className="bikes">
      <div className="hero">
        <h2>Nos vélos — Choisissez le vôtre</h2>
        <p>Tarifs en FCFA | Réservation simple et rapide</p>
      </div>

      <div className="bike-grid">
        {loading ? Array.from({length:6}).map((_,i)=> (
          <div key={i} className="bike-card" style={{padding:12}}>
            <div className="skeleton" style={{height:160}}></div>
            <div style={{padding:12}}>
              <div className="skeleton" style={{height:18, width:'60%'}}></div>
              <div style={{height:8}}></div>
              <div className="skeleton" style={{height:12, width:'80%'}}></div>
            </div>
          </div>
        )) : bikes.map(b=> (
          // apply simple client-side filter
          filter && !(b.name.toLowerCase().includes(filter.toLowerCase()) || (b.description || '').toLowerCase().includes(filter.toLowerCase())) ? null : (
          <article key={b.id} className="bike-card">
            <img src={b.image_url} alt={b.name} />
            <div className="meta">
              <h3>{b.name}</h3>
              <p style={{color:'#666'}}>{b.description}</p>
              <div style={{display:'flex', justifyContent:'space-between', alignItems:'center'}}>
                <p className="price">{b.price_per_hour} {b.currency}/heure</p>
                <div style={{display:'flex', gap:8, alignItems:'center'}}>
                  <div style={{background:'#fff7f0', color:'#ff6b3b', padding:'4px 8px', borderRadius:8, fontWeight:700}}>Top</div>
                  <div style={{color:'#f59e0b'}}>★ 4.8</div>
                </div>
              </div>
              <div style={{display:'flex', justifyContent:'flex-end'}}>
                <a className="btn" href={`#/reserve/${b.id}`}>Réserver</a>
              </div>
            </div>
          </article>
          )
        ))}
      </div>
    </section>
  )
}
