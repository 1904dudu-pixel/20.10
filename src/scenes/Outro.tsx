import {content} from '../data/content';
import {palette, Rise, SceneFrame} from '../components/SceneFrame';

export const Outro = () => (
  <SceneFrame dark>
    <div style={{position: 'absolute', left: 280, right: 280, top: 295, textAlign: 'center'}}>
      <Rise style={{fontSize: 29, letterSpacing: 8, color: '#d7c69f'}}>HAPPY VIETNAMESE WOMEN’S DAY</Rise>
      <Rise delay={0.25} style={{marginTop: 58, fontSize: 130, fontFamily: 'Georgia, "DejaVu Serif", serif', lineHeight: 1.28}}>
        {content.outroTitle}<br /><span style={{fontStyle: 'italic', color: palette.pink}}>{content.outroAccent}</span>
      </Rise>
      <Rise delay={0.7} style={{marginTop: 50, fontSize: 43, lineHeight: 1.65, whiteSpace: 'pre-line', color: '#d8e6d9'}}>{content.outroMessage}</Rise>
      <Rise delay={1.1} style={{marginTop: 60, fontSize: 29, letterSpacing: 2, color: '#d7c69f'}}>{content.signature}</Rise>
    </div>
  </SceneFrame>
);
