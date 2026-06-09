import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/client';

export default function Home() {
  const [data, setData] = useState(null);

  useEffect(() => { API.get('/home/').then(r => setData(r.data)); }, []);

  if (!data) return <div style={s.loading}>Loading...</div>;

  return (
    <div>
      {/* Hero */}
      <section style={s.hero}>
        <div style={s.heroInner}>
          <div style={s.heroTag}>🏢 MSME Registered · Kalaburagi, Karnataka, India</div>
          <h1 style={s.heroH1}>We Turn Students<br /><span style={s.accent}>Into Professionals</span></h1>
          <p style={s.heroSub}>Vignan TechSolutions bridges the gap between <strong>education and employment</strong> — through hands-on internships, industry courses, real-time projects, and corporate training.</p>
          <div style={s.heroCta}>
            <Link to="/internships" style={s.btnPrimary}>🚀 Start Your Journey</Link>
            <Link to="/about" style={s.btnGhost}>▶ Our Story</Link>
          </div>
        </div>
      </section>

      {/* Featured Projects */}
      {data.featured_projects?.length > 0 && (
        <section style={s.section}>
          <div style={s.container}>
            <div style={s.sectionHead}>
              <span style={s.badge}>⭐ Our Core Offering</span>
              <h2 style={s.sectionTitle}>MCA Major Projects</h2>
              <p style={s.sectionSub}>75+ end-to-end project services for VTU CPGS Kalaburagi</p>
            </div>
            <div style={s.grid3}>
              {data.featured_projects.map(p => (
                <Link to={`/projects/${p.slug}`} key={p.id} style={s.card}>
                  <div style={{...s.cardThumb, background: p.domain?.gradient || 'linear-gradient(135deg,#1E3A8A,#3B82F6)'}}>
                    {p.thumbnail ? <img src={p.thumbnail} alt={p.title} style={s.thumbImg} /> : <span style={s.emoji}>{p.domain?.emoji || '💻'}</span>}
                  </div>
                  <div style={s.cardBody}>
                    <span style={s.cardCat}>{p.domain?.name}</span>
                    <h4 style={s.cardTitle}>{p.title}</h4>
                    <p style={s.cardDesc}>{p.description?.split(' ').slice(0, 15).join(' ')}...</p>
                    <div style={s.tags}>{p.tech_stack_list?.slice(0, 3).map(t => <span key={t} style={s.tag}>{t}</span>)}</div>
                  </div>
                </Link>
              ))}
            </div>
            <div style={{textAlign:'center', marginTop:'2rem'}}>
              <Link to="/projects" style={s.btnPrimary}>Browse All {data.project_total}+ Projects →</Link>
            </div>
          </div>
        </section>
      )}

      {/* Featured Internships */}
      {data.featured_internships?.length > 0 && (
        <section style={{...s.section, background:'#fff'}}>
          <div style={s.container}>
            <div style={s.sectionHead}>
              <span style={s.badge}>Live Opportunities</span>
              <h2 style={s.sectionTitle}>Featured Internships</h2>
            </div>
            <div style={s.grid4}>
              {data.featured_internships.map(i => (
                <div key={i.id} style={s.card}>
                  <div style={{...s.cardThumb, background:'linear-gradient(135deg,#1E3A8A,#3B82F6)'}}>
                    {i.thumbnail ? <img src={i.thumbnail} alt={i.title} style={s.thumbImg} /> : <span style={s.emoji}>💼</span>}
                    <span style={s.modeBadge}>{i.mode_display}</span>
                  </div>
                  <div style={s.cardBody}>
                    <h4 style={s.cardTitle}>{i.title}</h4>
                    <p style={s.cardDesc}>{i.description?.split(' ').slice(0, 15).join(' ')}...</p>
                    <div style={s.cardMeta}><span>⏱ {i.duration}</span><span>👥 {i.seats_available} seats</span></div>
                  </div>
                  <Link to={`/internships/${i.slug}`} style={s.cardBtn}>Enroll Now</Link>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Featured Courses */}
      {data.featured_courses?.length > 0 && (
        <section style={s.section}>
          <div style={s.container}>
            <div style={s.sectionHead}>
              <span style={s.badge}>Industry Courses</span>
              <h2 style={s.sectionTitle}>Learn From the Best</h2>
            </div>
            <div style={s.grid3}>
              {data.featured_courses.map(c => (
                <div key={c.id} style={s.card}>
                  <div style={{...s.cardThumb, background:'linear-gradient(135deg,#059669,#10B981)'}}>
                    {c.thumbnail ? <img src={c.thumbnail} alt={c.title} style={s.thumbImg} /> : <span style={s.emoji}>📚</span>}
                    <span style={s.modeBadge}>{c.level_display}</span>
                  </div>
                  <div style={s.cardBody}>
                    <h4 style={s.cardTitle}>{c.title}</h4>
                    <p style={s.cardDesc}>{c.description?.split(' ').slice(0, 15).join(' ')}...</p>
                    <div style={s.cardMeta}><span>⏱ {c.duration}</span><span>👤 {c.instructor}</span></div>
                  </div>
                  <Link to={`/courses/${c.slug}`} style={s.cardBtn}>Enroll Now</Link>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Testimonials */}
      {data.testimonials?.length > 0 && (
        <section style={{...s.section, background:'#fff'}}>
          <div style={s.container}>
            <div style={s.sectionHead}>
              <span style={s.badge}>Student Reviews</span>
              <h2 style={s.sectionTitle}>What Our Students Say</h2>
            </div>
            <div style={s.grid3}>
              {data.testimonials.map(t => (
                <div key={t.id} style={s.testimonialCard}>
                  <div style={s.stars}>{'⭐'.repeat(t.rating)}</div>
                  <p style={s.testimonialText}>"{t.message}"</p>
                  <div style={s.testimonialAuthor}>
                    <div style={s.avatar}>{t.name?.[0]}</div>
                    <div>
                      <div style={{fontWeight:700, fontSize:'.9rem'}}>{t.name}</div>
                      <div style={{color:'#6B7280', fontSize:'.8rem'}}>{t.designation}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section style={s.cta}>
        <div style={s.container}>
          <h2 style={{color:'#fff', fontSize:'2rem', fontWeight:800, marginBottom:'1rem'}}>Need Your Major Project Done Right?</h2>
          <p style={{color:'rgba(255,255,255,.75)', marginBottom:'1.5rem'}}>Complete source code · IEEE documentation · Demo video · 1-on-1 mentorship</p>
          <div style={{display:'flex', gap:'1rem', justifyContent:'center', flexWrap:'wrap'}}>
            <Link to="/projects" style={s.btnWhite}>Browse All Projects</Link>
            <a href="https://wa.me/919110478047" target="_blank" rel="noopener" style={s.btnWa}>💬 WhatsApp Us</a>
          </div>
        </div>
      </section>
    </div>
  );
}

const s = {
  loading: { textAlign:'center', padding:'4rem', fontSize:'1.2rem', color:'#6B7280' },
  hero: { background:'linear-gradient(135deg,#0F172A 0%,#1E3A8A 50%,#0F172A 100%)', minHeight:'80vh', display:'flex', alignItems:'center', padding:'4rem 0' },
  heroInner: { maxWidth:700, margin:'0 auto', textAlign:'center', padding:'0 1.5rem' },
  heroTag: { color:'rgba(255,255,255,.6)', fontSize:'.85rem', marginBottom:'1rem' },
  heroH1: { fontSize:'clamp(2rem,5vw,3.5rem)', fontWeight:800, color:'#fff', lineHeight:1.2, marginBottom:'1rem' },
  accent: { color:'#60A5FA' },
  heroSub: { color:'rgba(255,255,255,.75)', fontSize:'1.05rem', lineHeight:1.8, marginBottom:'2rem' },
  heroCta: { display:'flex', gap:'1rem', justifyContent:'center', flexWrap:'wrap' },
  btnPrimary: { background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', padding:'.75rem 2rem', borderRadius:50, fontWeight:700, textDecoration:'none', fontSize:'.95rem' },
  btnGhost: { background:'rgba(255,255,255,.1)', color:'#fff', padding:'.75rem 2rem', borderRadius:50, fontWeight:700, textDecoration:'none', fontSize:'.95rem', border:'1px solid rgba(255,255,255,.2)' },
  section: { padding:'4rem 0', background:'#F8FAFC' },
  container: { maxWidth:1200, margin:'0 auto', padding:'0 1.5rem' },
  sectionHead: { textAlign:'center', marginBottom:'2.5rem' },
  badge: { background:'rgba(30,58,138,.08)', color:'#1E3A8A', padding:'4px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700 },
  sectionTitle: { fontSize:'2rem', fontWeight:800, color:'#0F172A', margin:'.5rem 0' },
  sectionSub: { color:'#6B7280', fontSize:'1rem' },
  grid3: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(300px,1fr))', gap:'1.5rem' },
  grid4: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(240px,1fr))', gap:'1.5rem' },
  card: { background:'#fff', borderRadius:16, overflow:'hidden', boxShadow:'0 4px 16px rgba(0,0,0,.06)', textDecoration:'none', color:'inherit', display:'flex', flexDirection:'column' },
  cardThumb: { height:180, display:'flex', alignItems:'center', justifyContent:'center', position:'relative' },
  thumbImg: { width:'100%', height:'100%', objectFit:'cover' },
  emoji: { fontSize:'3.5rem' },
  modeBadge: { position:'absolute', top:10, right:10, background:'rgba(0,0,0,.5)', color:'#fff', padding:'3px 10px', borderRadius:50, fontSize:'.72rem', fontWeight:700 },
  cardBody: { padding:'1.25rem', flex:1 },
  cardCat: { color:'#3B82F6', fontSize:'.75rem', fontWeight:700, textTransform:'uppercase', letterSpacing:'.05em' },
  cardTitle: { fontWeight:700, fontSize:'1rem', margin:'.4rem 0', color:'#0F172A' },
  cardDesc: { color:'#6B7280', fontSize:'.85rem', lineHeight:1.7 },
  cardMeta: { display:'flex', gap:'1rem', color:'#6B7280', fontSize:'.8rem', marginTop:'.75rem' },
  tags: { display:'flex', flexWrap:'wrap', gap:'.4rem', marginTop:'.75rem' },
  tag: { background:'#EEF2FF', color:'#4F46E5', padding:'2px 10px', borderRadius:50, fontSize:'.72rem', fontWeight:600 },
  cardBtn: { display:'block', textAlign:'center', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', padding:'.75rem', fontWeight:700, textDecoration:'none', fontSize:'.88rem' },
  testimonialCard: { background:'#F8FAFC', border:'1px solid #E2E8F0', borderRadius:16, padding:'1.5rem' },
  stars: { fontSize:'1rem', marginBottom:'.75rem' },
  testimonialText: { color:'#475569', fontSize:'.9rem', lineHeight:1.8, marginBottom:'1.25rem' },
  testimonialAuthor: { display:'flex', alignItems:'center', gap:'.75rem' },
  avatar: { width:40, height:40, borderRadius:'50%', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', display:'flex', alignItems:'center', justifyContent:'center', color:'#fff', fontWeight:800, fontSize:'1rem', flexShrink:0 },
  cta: { background:'linear-gradient(135deg,#0F172A,#1E3A8A)', padding:'4rem 0', textAlign:'center' },
  btnWhite: { background:'#fff', color:'#1E3A8A', padding:'.75rem 2rem', borderRadius:50, fontWeight:700, textDecoration:'none', fontSize:'.95rem' },
  btnWa: { background:'#25D366', color:'#fff', padding:'.75rem 2rem', borderRadius:50, fontWeight:700, textDecoration:'none', fontSize:'.95rem' },
};
