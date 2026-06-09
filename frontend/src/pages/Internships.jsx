import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/client';

export default function Internships() {
  const [internships, setInternships] = useState([]);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState('');

  useEffect(() => {
    API.get('/internships/', { params: mode ? { mode } : {} })
      .then(r => setInternships(r.data.results || r.data))
      .finally(() => setLoading(false));
  }, [mode]);

  return (
    <div style={s.page}>
      <div style={s.container}>
        <div style={s.header}>
          <span style={s.badge}>Live Opportunities</span>
          <h1 style={s.title}>Internship Programs</h1>
          <p style={s.sub}>Real work. Real experience. Real certificate.</p>
          <div style={s.filters}>
            {['', 'online', 'offline', 'hybrid'].map(m => (
              <button key={m} style={{...s.pill, ...(mode === m ? s.pillActive : {})}} onClick={() => setMode(m)}>
                {m ? m.charAt(0).toUpperCase() + m.slice(1) : 'All'}
              </button>
            ))}
          </div>
        </div>
        {loading ? <div style={s.loading}>Loading internships...</div> : (
          <div style={s.grid}>
            {internships.map(i => (
              <div key={i.id} style={s.card}>
                <div style={{...s.thumb, background:'linear-gradient(135deg,#1E3A8A,#3B82F6)'}}>
                  {i.thumbnail ? <img src={i.thumbnail} alt={i.title} style={s.img} /> : <span style={s.emoji}>💼</span>}
                  <span style={s.modeBadge}>{i.mode_display}</span>
                </div>
                <div style={s.body}>
                  <h3 style={s.cardTitle}>{i.title}</h3>
                  <p style={s.desc}>{i.description?.split(' ').slice(0, 15).join(' ')}...</p>
                  <div style={s.meta}><span>⏱ {i.duration}</span><span>👥 {i.seats_available} seats</span><span style={s.fee}>₹{i.fees}</span></div>
                </div>
                <Link to={`/internships/${i.slug}`} style={s.btn}>Enroll Now</Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const s = {
  page: { background:'#F8FAFC', minHeight:'80vh', padding:'3rem 0' },
  container: { maxWidth:1200, margin:'0 auto', padding:'0 1.5rem' },
  header: { textAlign:'center', marginBottom:'3rem' },
  badge: { background:'rgba(30,58,138,.08)', color:'#1E3A8A', padding:'4px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700 },
  title: { fontSize:'2.5rem', fontWeight:800, color:'#0F172A', margin:'.5rem 0' },
  sub: { color:'#6B7280', marginBottom:'1.5rem' },
  filters: { display:'flex', gap:'.5rem', justifyContent:'center', flexWrap:'wrap' },
  pill: { padding:'.4rem 1.1rem', borderRadius:50, border:'1.5px solid #E2E8F0', background:'#fff', cursor:'pointer', fontWeight:600, fontSize:'.82rem', color:'#374151' },
  pillActive: { background:'#1E3A8A', color:'#fff', borderColor:'#1E3A8A' },
  loading: { textAlign:'center', padding:'3rem', color:'#6B7280' },
  grid: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(280px,1fr))', gap:'1.5rem' },
  card: { background:'#fff', borderRadius:16, overflow:'hidden', boxShadow:'0 4px 16px rgba(0,0,0,.06)', display:'flex', flexDirection:'column' },
  thumb: { height:180, display:'flex', alignItems:'center', justifyContent:'center', position:'relative' },
  img: { width:'100%', height:'100%', objectFit:'cover' },
  emoji: { fontSize:'4rem' },
  modeBadge: { position:'absolute', top:10, right:10, background:'rgba(0,0,0,.5)', color:'#fff', padding:'3px 10px', borderRadius:50, fontSize:'.72rem', fontWeight:700 },
  body: { padding:'1.25rem', flex:1 },
  cardTitle: { fontWeight:700, fontSize:'1rem', margin:'0 0 .5rem', color:'#0F172A' },
  desc: { color:'#6B7280', fontSize:'.85rem', lineHeight:1.7, marginBottom:'.75rem' },
  meta: { display:'flex', gap:'1rem', color:'#6B7280', fontSize:'.8rem', flexWrap:'wrap' },
  fee: { color:'#1E3A8A', fontWeight:700 },
  btn: { display:'block', textAlign:'center', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', padding:'.75rem', fontWeight:700, textDecoration:'none', fontSize:'.88rem' },
};
