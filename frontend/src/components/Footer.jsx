import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer style={s.footer}>
      <div style={s.container}>
        <div style={s.grid}>
          <div>
            <div style={s.brand}>Vignan TechSolutions</div>
            <p style={s.desc}>Empowering students and professionals with industry-ready skills through internships, courses, and corporate training.</p>
            <div style={s.badges}>
              <span style={s.badge}>✅ MSME Registered</span>
              <span style={s.badge}>🛡️ ISO Certified</span>
            </div>
          </div>
          <div>
            <div style={s.heading}>Quick Links</div>
            {[['/', 'Home'], ['/about', 'About Us'], ['/internships', 'Internships'],
              ['/courses', 'Courses'], ['/projects', 'Projects'], ['/contact', 'Contact']
            ].map(([to, label]) => <Link key={to} to={to} style={s.link}>{label}</Link>)}
          </div>
          <div>
            <div style={s.heading}>Services</div>
            {['/internships', '/courses', '/corporate-training', '/projects', '/contact', '/certificates/verify'].map((to, i) => (
              <Link key={to} to={to} style={s.link}>
                {['Internship Programs','Professional Courses','Corporate Training','Real-Time Projects','Software Development','Verify Certificate'][i]}
              </Link>
            ))}
          </div>
          <div>
            <div style={s.heading}>Contact Info</div>
            <p style={s.info}>📍 Kalaburagi, Karnataka, India</p>
            <p style={s.info}>📞 +91-9110478047</p>
            <p style={s.info}>📞 +91-9148215446</p>
            <p style={s.info}>✉️ vignantechsolutions@gmail.com</p>
            <p style={s.info}>🕐 Mon–Sat: 9AM – 6PM IST</p>
          </div>
        </div>
        <hr style={{borderColor:'#1E293B', margin:'1.5rem 0'}} />
        <div style={s.bottom}>
          <span>© 2025 Vignan TechSolutions. All rights reserved.</span>
          <div style={{display:'flex', gap:'1rem'}}>
            <a href="/sitemap.xml" style={s.link}>Sitemap</a>
            <Link to="/certificates/verify" style={s.link}>Verify Certificate</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

const s = {
  footer: { background:'#0F172A', color:'#fff', paddingTop:'3rem', marginTop:'4rem' },
  container: { maxWidth:1200, margin:'0 auto', padding:'0 1.5rem 1.5rem' },
  grid: { display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(200px,1fr))', gap:'2rem' },
  brand: { fontWeight:800, fontSize:'1.1rem', color:'#3B82F6', marginBottom:'.75rem' },
  desc: { color:'#94A3B8', fontSize:'.85rem', lineHeight:1.7, maxWidth:280 },
  badges: { display:'flex', gap:'.5rem', flexWrap:'wrap', marginTop:'.75rem' },
  badge: { background:'rgba(59,130,246,.15)', color:'#93C5FD', border:'1px solid rgba(59,130,246,.2)', borderRadius:50, padding:'3px 10px', fontSize:'.72rem', fontWeight:600 },
  heading: { color:'#3B82F6', fontWeight:700, fontSize:'.75rem', letterSpacing:'.08em', textTransform:'uppercase', marginBottom:'.75rem' },
  link: { display:'block', color:'#CBD5E1', textDecoration:'none', fontSize:'.85rem', marginBottom:'.4rem' },
  info: { color:'#CBD5E1', fontSize:'.85rem', marginBottom:'.4rem' },
  bottom: { display:'flex', justifyContent:'space-between', alignItems:'center', flexWrap:'wrap', gap:'1rem', color:'#64748B', fontSize:'.82rem' },
};
