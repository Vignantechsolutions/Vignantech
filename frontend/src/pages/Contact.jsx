import { useState } from 'react';
import API from '../api/client';
import toast from 'react-hot-toast';

export function Contact() {
  const [form, setForm] = useState({ name:'', email:'', phone:'', subject:'', message:'' });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await API.post('/contact/', form);
      toast.success('Message sent! We will get back to you soon.');
      setForm({ name:'', email:'', phone:'', subject:'', message:'' });
    } catch { toast.error('Failed to send. Please try again.'); }
    finally { setLoading(false); }
  };

  return (
    <div style={s.page}>
      <div style={s.container}>
        <div style={s.header}>
          <h1 style={s.title}>Get In Touch</h1>
          <p style={s.sub}>Have a question? We'd love to hear from you.</p>
        </div>
        <div style={s.grid}>
          <div style={s.info}>
            {[['📍','Address','Kalaburagi, Karnataka, India'],['📞','Phone','+91-9110478047 / +91-9148215446'],['✉️','Email','vignantechsolutions@gmail.com'],['🕐','Hours','Mon–Sat: 9AM – 6PM IST']].map(([icon, label, val]) => (
              <div key={label} style={s.infoItem}>
                <span style={s.infoIcon}>{icon}</span>
                <div><div style={s.infoLabel}>{label}</div><div style={s.infoVal}>{val}</div></div>
              </div>
            ))}
            <a href="https://wa.me/919110478047" target="_blank" rel="noopener" style={s.waBtn}>💬 WhatsApp Us Now</a>
          </div>
          <form onSubmit={handleSubmit} style={s.form}>
            <div style={s.row}>
              <div style={{flex:1}}><label style={s.label}>Name</label><input style={s.input} value={form.name} onChange={e=>setForm({...form,name:e.target.value})} required /></div>
              <div style={{flex:1}}><label style={s.label}>Email</label><input style={s.input} type="email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required /></div>
            </div>
            <label style={s.label}>Phone</label>
            <input style={s.input} value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} />
            <label style={s.label}>Subject</label>
            <input style={s.input} value={form.subject} onChange={e=>setForm({...form,subject:e.target.value})} required />
            <label style={s.label}>Message</label>
            <textarea style={{...s.input, height:120, resize:'vertical'}} value={form.message} onChange={e=>setForm({...form,message:e.target.value})} required />
            <button type="submit" style={s.btn} disabled={loading}>{loading ? 'Sending...' : 'Send Message'}</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export function CertificateVerify() {
  const [certId, setCertId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleVerify = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await API.get(`/certificates/verify/${certId}/`);
      setResult({ valid: true, data });
    } catch { setResult({ valid: false }); }
    finally { setLoading(false); }
  };

  return (
    <div style={s.page}>
      <div style={{...s.container, maxWidth:600}}>
        <div style={s.header}>
          <span style={s.badge}>🏆 Certificate Verification</span>
          <h1 style={s.title}>Verify Certificate</h1>
          <p style={s.sub}>Enter the Certificate ID to verify its authenticity</p>
        </div>
        <form onSubmit={handleVerify} style={s.verifyForm}>
          <input style={s.verifyInput} value={certId} onChange={e=>setCertId(e.target.value)} placeholder="Enter Certificate ID (UUID format)" required />
          <button type="submit" style={s.btn} disabled={loading}>{loading ? 'Verifying...' : 'Verify Certificate'}</button>
        </form>
        {result && (
          <div style={{...s.resultBox, borderColor: result.valid ? '#10B981' : '#EF4444'}}>
            {result.valid ? (
              <>
                <div style={{color:'#10B981', fontSize:'2rem', marginBottom:'.5rem'}}>✅ Valid Certificate</div>
                <div style={s.resultName}>{result.data.enrollment?.course?.title || result.data.enrollment?.internship?.title}</div>
                <div style={s.resultSub}>Issued: {new Date(result.data.issued_date).toLocaleDateString()}</div>
              </>
            ) : (
              <div style={{color:'#EF4444', fontSize:'1.2rem'}}>❌ Invalid or expired certificate</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

const s = {
  page: { background:'#F8FAFC', minHeight:'80vh', padding:'3rem 0' },
  container: { maxWidth:1100, margin:'0 auto', padding:'0 1.5rem' },
  header: { textAlign:'center', marginBottom:'2.5rem' },
  badge: { background:'rgba(30,58,138,.08)', color:'#1E3A8A', padding:'4px 14px', borderRadius:50, fontSize:'.8rem', fontWeight:700 },
  title: { fontSize:'2.5rem', fontWeight:800, color:'#0F172A', margin:'.5rem 0' },
  sub: { color:'#6B7280' },
  grid: { display:'grid', gridTemplateColumns:'1fr 1.5fr', gap:'2.5rem', alignItems:'start' },
  info: { background:'#fff', borderRadius:16, padding:'2rem', boxShadow:'0 4px 16px rgba(0,0,0,.06)' },
  infoItem: { display:'flex', gap:'1rem', alignItems:'flex-start', marginBottom:'1.5rem' },
  infoIcon: { fontSize:'1.5rem', flexShrink:0 },
  infoLabel: { fontWeight:700, fontSize:'.85rem', color:'#374151' },
  infoVal: { color:'#6B7280', fontSize:'.9rem', marginTop:'.15rem' },
  waBtn: { display:'block', textAlign:'center', background:'#25D366', color:'#fff', padding:'.75rem', borderRadius:10, fontWeight:700, textDecoration:'none', marginTop:'1.5rem' },
  form: { background:'#fff', borderRadius:16, padding:'2rem', boxShadow:'0 4px 16px rgba(0,0,0,.06)' },
  row: { display:'flex', gap:'1rem' },
  label: { display:'block', fontWeight:600, fontSize:'.85rem', color:'#374151', marginBottom:'.4rem' },
  input: { width:'100%', border:'1.5px solid #E2E8F0', borderRadius:10, padding:'.7rem 1rem', fontSize:'.95rem', marginBottom:'1rem', boxSizing:'border-box', outline:'none' },
  btn: { width:'100%', background:'linear-gradient(135deg,#1E3A8A,#3B82F6)', color:'#fff', border:'none', borderRadius:10, padding:'.85rem', fontSize:'1rem', fontWeight:700, cursor:'pointer' },
  verifyForm: { display:'flex', gap:'1rem', marginBottom:'2rem', flexWrap:'wrap' },
  verifyInput: { flex:1, border:'1.5px solid #E2E8F0', borderRadius:10, padding:'.7rem 1rem', fontSize:'.95rem', outline:'none', minWidth:200 },
  resultBox: { background:'#fff', border:'2px solid', borderRadius:16, padding:'2rem', textAlign:'center', boxShadow:'0 4px 16px rgba(0,0,0,.06)' },
  resultName: { fontWeight:700, fontSize:'1.1rem', color:'#0F172A', marginTop:'.5rem' },
  resultSub: { color:'#6B7280', marginTop:'.25rem' },
};
