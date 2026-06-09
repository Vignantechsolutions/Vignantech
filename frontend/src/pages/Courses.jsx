import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/client';

export default function Courses() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [level, setLevel] = useState('');

  useEffect(() => {
    API.get('/courses/', { params: level ? { level } : {} })
      .then(r => setCourses(r.data.results || r.data))
      .finally(() => setLoading(false));
  }, [level]);

  return (
    <div style={s.page}>
      <div style={s.container}>
        <div style={s.header}>
          <span style={s.badge}>Industry Courses</span>
          <h1 style={s.title}>Professional Courses</h1>
          <p style={s.sub}>Industry-aligned courses built around what companies actually hire for</p>
          <div style={s.filters}>
            {['', 'beginner', 'intermediate', 'advanced'].map(l => (
              <button key={l} style={{...s.pill, ...(level === l ? s.pillActive : {})}} onClick={() => setLevel(l)}>
                {l ? l.charAt(0).toUpperCase() + l.slice(1) : 'All Levels'}
              </button>
            ))}
          </div>
        </div>
        {loading ? <div style={s.loading}>Loading courses...</div> : (
          <div style={s.grid}>
            {courses.map(c => (
              <div key={c.id} style={s.card}>
                <div style={{...s.thumb, background:'linear-gradient(135deg,#059669,#10B981)'}}>
                  {c.thumbnail ? <img src={c.thumbnail} alt={c.title} style={s.img} /> : <span style={s.emoji}>📚</span>}
                  <span style={s.levelBadge}>{c.level_display}</span>
                </div>
                <div style={s.body}>
                  <h3 style={s.cardTitle}>{c.title}</h3>
                  <p style={s.desc}>{c.description?.split(' ').slice(0, 15).join(' ')}...</p>
                  <div style={s.meta}><span>⏱ {c.duration}</span><span>👤 {c.instructor}</span><span style={s.fee}>₹{c.fees}</span></div>
                </div>
                <Link to={`/courses/${c.slug}`} style={s.btn}>View Course</Link>
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
  badge: { background:'rgba(5,150,105,.1)', color:'#059669', padding:'4px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700 },
  title: { fontSize:'2.5rem', fontWeight:800, color:'#0F172A', margin:'.5rem 0' },
  sub: { color:'#6B7280', marginBottom:'1.5rem' },
  filters: { display:'flex', gap:'.5rem', justifyContent:'center', flexWrap:'wrap' },
  pill: { padding:'.4rem 1.1rem', borderRadius:50, border:'1.5px solid #E2E8F0', background:'#fff', cursor:'pointer', fontWeight:600, fontSize:'.82rem', color:'#374151' },
  pillActive: { background:'#059669', color:'#fff', borderColor:'#059669' },
  loading: { textAlign:'center', padding:'3rem', color:'#6B7280' },
  grid: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(300px,1fr))', gap:'1.5rem' },
  card: { background:'#fff', borderRadius:16, overflow:'hidden', boxShadow:'0 4px 16px rgba(0,0,0,.06)', display:'flex', flexDirection:'column' },
  thumb: { height:180, display:'flex', alignItems:'center', justifyContent:'center', position:'relative' },
  img: { width:'100%', height:'100%', objectFit:'cover' },
  emoji: { fontSize:'4rem' },
  levelBadge: { position:'absolute', top:10, right:10, background:'rgba(5,150,105,.9)', color:'#fff', padding:'3px 10px', borderRadius:50, fontSize:'.72rem', fontWeight:700 },
  body: { padding:'1.25rem', flex:1 },
  cardTitle: { fontWeight:700, fontSize:'1rem', margin:'0 0 .5rem', color:'#0F172A' },
  desc: { color:'#6B7280', fontSize:'.85rem', lineHeight:1.7, marginBottom:'.75rem' },
  meta: { display:'flex', gap:'1rem', color:'#6B7280', fontSize:'.8rem', flexWrap:'wrap' },
  fee: { color:'#059669', fontWeight:700 },
  btn: { display:'block', textAlign:'center', background:'linear-gradient(135deg,#059669,#10B981)', color:'#fff', padding:'.75rem', fontWeight:700, textDecoration:'none', fontSize:'.88rem' },
};
