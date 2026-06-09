import { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import API from '../api/client';

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [params, setParams] = useSearchParams();
  const category = params.get('category') || '';

  useEffect(() => {
    Promise.all([
      API.get('/projects/', { params: { category: category || undefined } }),
      API.get('/domains/'),
    ]).then(([p, d]) => {
      setProjects(p.data.results || p.data);
      setDomains(d.data.results || d.data);
    }).finally(() => setLoading(false));
  }, [category]);

  return (
    <div style={s.page}>
      <div style={s.container}>
        <div style={s.header}>
          <span style={s.badge}>75+ Projects</span>
          <h1 style={s.title}>MCA Major Projects</h1>
          <p style={s.sub}>End-to-end project services for VTU CPGS Kalaburagi across 5 domains</p>
          <div style={s.domainPills}>
            <button style={{...s.pill, ...(category === '' ? s.pillActive : {})}} onClick={() => setParams({})}>All</button>
            {domains.map(d => (
              <button key={d.slug} style={{...s.pill, ...(category === d.slug ? s.pillActive : {})}}
                onClick={() => setParams({ category: d.slug })}>
                {d.emoji} {d.name}
              </button>
            ))}
          </div>
        </div>

        {loading ? <div style={s.loading}>Loading projects...</div> : (
          <div style={s.grid}>
            {projects.map(p => (
              <Link to={`/projects/${p.slug}`} key={p.id} style={s.card}>
                <div style={{...s.thumb, background: p.domain?.gradient || 'linear-gradient(135deg,#1E3A8A,#3B82F6)'}}>
                  {p.thumbnail ? <img src={p.thumbnail} alt={p.title} style={s.img} /> : <span style={s.emoji}>{p.domain?.emoji || '💻'}</span>}
                </div>
                <div style={s.body}>
                  <span style={s.cat}>{p.domain?.name}</span>
                  <h3 style={s.cardTitle}>{p.title}</h3>
                  <p style={s.desc}>{p.description?.split(' ').slice(0, 15).join(' ')}...</p>
                  <div style={s.tags}>{p.tech_stack_list?.slice(0, 4).map(t => <span key={t} style={s.tag}>{t}</span>)}</div>
                </div>
              </Link>
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
  badge: { background:'rgba(124,58,237,.1)', color:'#7C3AED', padding:'4px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700 },
  title: { fontSize:'2.5rem', fontWeight:800, color:'#0F172A', margin:'.5rem 0' },
  sub: { color:'#6B7280', fontSize:'1rem', marginBottom:'1.5rem' },
  domainPills: { display:'flex', gap:'.5rem', justifyContent:'center', flexWrap:'wrap' },
  pill: { padding:'.4rem 1.1rem', borderRadius:50, border:'1.5px solid #E2E8F0', background:'#fff', cursor:'pointer', fontWeight:600, fontSize:'.82rem', color:'#374151' },
  pillActive: { background:'#1E3A8A', color:'#fff', borderColor:'#1E3A8A' },
  loading: { textAlign:'center', padding:'3rem', color:'#6B7280' },
  grid: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(300px,1fr))', gap:'1.5rem' },
  card: { background:'#fff', borderRadius:16, overflow:'hidden', boxShadow:'0 4px 16px rgba(0,0,0,.06)', textDecoration:'none', color:'inherit' },
  thumb: { height:180, display:'flex', alignItems:'center', justifyContent:'center' },
  img: { width:'100%', height:'100%', objectFit:'cover' },
  emoji: { fontSize:'4rem' },
  body: { padding:'1.25rem' },
  cat: { color:'#7C3AED', fontSize:'.75rem', fontWeight:700, textTransform:'uppercase' },
  cardTitle: { fontWeight:700, fontSize:'1rem', margin:'.4rem 0', color:'#0F172A' },
  desc: { color:'#6B7280', fontSize:'.85rem', lineHeight:1.7 },
  tags: { display:'flex', flexWrap:'wrap', gap:'.4rem', marginTop:'.75rem' },
  tag: { background:'#EEF2FF', color:'#4F46E5', padding:'2px 10px', borderRadius:50, fontSize:'.72rem', fontWeight:600 },
};
