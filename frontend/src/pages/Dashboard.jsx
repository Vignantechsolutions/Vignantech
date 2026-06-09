import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../api/client';
import { useAuth } from '../context/AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState(null);

  useEffect(() => { API.get('/dashboard/').then(r => setData(r.data)); }, []);

  if (!data) return <div style={s.loading}>Loading dashboard...</div>;

  return (
    <div style={s.page}>
      <div style={s.container}>
        <h1 style={s.title}>Welcome back, {user?.name?.split(' ')[0]}! 👋</h1>
        <div style={s.statsGrid}>
          {[
            { label:'Active Enrollments', value: data.stats.active, color:'#3B82F6' },
            { label:'Completed', value: data.stats.completed, color:'#10B981' },
            { label:'Certificates', value: data.stats.certificates, color:'#7C3AED' },
            { label:'Total Spent', value: `₹${data.stats.total_spent}`, color:'#F59E0B' },
          ].map(stat => (
            <div key={stat.label} style={{...s.statCard, borderTop:`4px solid ${stat.color}`}}>
              <div style={{...s.statValue, color: stat.color}}>{stat.value}</div>
              <div style={s.statLabel}>{stat.label}</div>
            </div>
          ))}
        </div>

        {data.enrollments.length > 0 && (
          <div style={s.section}>
            <h2 style={s.sectionTitle}>My Enrollments</h2>
            <div style={s.list}>
              {data.enrollments.map(e => (
                <div key={e.id} style={s.listItem}>
                  <div>
                    <div style={s.itemTitle}>{e.course?.title || e.internship?.title}</div>
                    <div style={s.itemSub}>{e.enrollment_type} · Enrolled {new Date(e.enrolled_at).toLocaleDateString()}</div>
                  </div>
                  <span style={{...s.statusBadge, background: e.status==='active'?'#D1FAE5':e.status==='completed'?'#DBEAFE':'#FEF3C7', color: e.status==='active'?'#059669':e.status==='completed'?'#1D4ED8':'#D97706'}}>
                    {e.status}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {data.certificates.length > 0 && (
          <div style={s.section}>
            <h2 style={s.sectionTitle}>My Certificates</h2>
            <div style={s.list}>
              {data.certificates.map(c => (
                <div key={c.id} style={s.listItem}>
                  <div>
                    <div style={s.itemTitle}>{c.enrollment?.course?.title || c.enrollment?.internship?.title}</div>
                    <div style={s.itemSub}>ID: {String(c.certificate_id).slice(0,8).toUpperCase()} · {new Date(c.issued_date).toLocaleDateString()}</div>
                  </div>
                  <a href={`/api/certificates/download/${c.certificate_id}/`} style={s.downloadBtn}>⬇ Download</a>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const s = {
  loading: { textAlign:'center', padding:'4rem', color:'#6B7280' },
  page: { background:'#F8FAFC', minHeight:'80vh', padding:'2.5rem 0' },
  container: { maxWidth:1000, margin:'0 auto', padding:'0 1.5rem' },
  title: { fontSize:'1.75rem', fontWeight:800, color:'#0F172A', marginBottom:'1.5rem' },
  statsGrid: { display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(200px,1fr))', gap:'1rem', marginBottom:'2rem' },
  statCard: { background:'#fff', borderRadius:12, padding:'1.25rem', boxShadow:'0 2px 8px rgba(0,0,0,.06)' },
  statValue: { fontSize:'2rem', fontWeight:800, lineHeight:1 },
  statLabel: { color:'#6B7280', fontSize:'.85rem', marginTop:'.25rem' },
  section: { background:'#fff', borderRadius:16, padding:'1.5rem', marginBottom:'1.5rem', boxShadow:'0 2px 8px rgba(0,0,0,.06)' },
  sectionTitle: { fontSize:'1.1rem', fontWeight:700, marginBottom:'1rem', color:'#0F172A' },
  list: { display:'flex', flexDirection:'column', gap:'.75rem' },
  listItem: { display:'flex', justifyContent:'space-between', alignItems:'center', padding:'.75rem', background:'#F8FAFC', borderRadius:10 },
  itemTitle: { fontWeight:600, color:'#0F172A', fontSize:'.95rem' },
  itemSub: { color:'#6B7280', fontSize:'.8rem', marginTop:'.2rem' },
  statusBadge: { padding:'3px 12px', borderRadius:50, fontSize:'.75rem', fontWeight:700, textTransform:'capitalize' },
  downloadBtn: { background:'#EEF2FF', color:'#4F46E5', padding:'5px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700, textDecoration:'none' },
};
