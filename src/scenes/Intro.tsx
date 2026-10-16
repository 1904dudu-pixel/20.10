import {content} from '../data/content';
import {palette, Rise, SceneFrame} from '../components/SceneFrame';

export const Intro = () => (
  <SceneFrame>
    <div style={{position: 'absolute', left: 210, top: 320, width: 1450}}>
      <Rise style={{fontSize: 29, letterSpacing: 7, color: '#688474'}}>{content.occasion}</Rise>
      <Rise delay={0.25} style={{marginTop: 58, fontFamily: 'Georgia, "DejaVu Serif", serif', fontSize: 134, lineHeight: 1.2}}>
        {content.introTitle}<br />
        <span style={{fontStyle: 'italic', color: '#648772'}}>{content.introAccent}</span>
      </Rise>
      <Rise delay={0.8} style={{marginTop: 60, fontSize: 43, lineHeight: 1.6, whiteSpace: 'pre-line'}}>{content.introMessage}</Rise>
    </div>
    <Rise delay={0.45} style={{position: 'absolute', right: 190, top: 380, width: 530, height: 600, border: `1px solid ${palette.gold}`, borderRadius: '265px 265px 20px 20px', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', background: '#ffffff35'}}>
      <span style={{fontSize: 150, fontFamily: 'Georgia, serif', lineHeight: 1.1}}>20</span>
      <span style={{width: 155, height: 1, background: palette.gold, margin: '30px 0'}} />
      <span style={{fontSize: 150, fontFamily: 'Georgia, serif', lineHeight: 1.1, color: '#70917e'}}>10</span>
      <span style={{fontSize: 22, letterSpacing: 5, marginTop: 36}}>DÀNH TẶNG BẠN</span>
    </Rise>
  </SceneFrame>
);
