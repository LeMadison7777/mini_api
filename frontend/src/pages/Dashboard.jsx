import React, {useEffect, useState} from 'react'

export default function Dashboard(){
  const [reservations, setReservations] = useState([])

  useEffect(()=>{
    fetch('/api/my_reservations', {credentials:'include'})
      .then(r=> r.json())
      .then(setReservations)
      .catch(()=> setReservations([]))
  },[])

  function logout(){
    fetch('/api/logout', {method:'POST', credentials:'include'})
      .then(()=> window.location.hash = '#/')
  }

  return (
    <section style={{maxWidth:900, margin:'20px auto'}}>
      <h2>Mes réservations</h2>
      <button className="btn" onClick={logout}>Se déconnecter</button>
      <ul style={{marginTop:12}}>
        {reservations.map(r=> (
          <li key={r.id}>Vélo #{r.bike_id} — {new Date(r.start).toLocaleString()} → {new Date(r.end).toLocaleString()}</li>
        ))}
      </ul>
    </section>
  )
}
