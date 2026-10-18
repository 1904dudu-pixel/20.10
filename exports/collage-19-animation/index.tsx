import React from 'react';
import {AbsoluteFill,CanvasImage,Composition,registerRoot,staticFile,useCurrentFrame,useVideoConfig} from 'remotion';
import spec from './spec.json';

const starPath='M0 -33 L1.4 -3.4 L11.7 -11.7 L3.4 -1.4 L33 0 L3.4 1.4 L11.7 11.7 L1.4 3.4 L0 33 L-1.4 3.4 L-11.7 11.7 L-3.4 1.4 L-33 0 L-3.4 -1.4 L-11.7 -11.7 L-1.4 -3.4 Z';
export const CollageSparkles: React.FC=()=>{
 const frame=useCurrentFrame();
 const {fps,durationInFrames}=useVideoConfig();
 const t=(frame%durationInFrames)/fps;
 const state=(p:typeof spec.dust[number])=>{
  const angle=2*Math.PI*(t/spec.durationSeconds*p.cycles+p.phase);
  const pulse=(1+Math.cos(2*Math.PI*(t/p.period+p.phase)))/2;
  return {x:p.x+p.dx*Math.sin(angle),y:p.y+p.dy*Math.cos(angle),pulse,angle};
 };
 return <AbsoluteFill>
  <CanvasImage src={staticFile(spec.posterFile)} premountFor={fps} style={{position:'absolute',width:'100%',height:'100%'}}/>
  <svg width={2560} height={1440} viewBox="0 0 2560 1440" style={{position:'absolute',inset:0}}>
   <defs>
    <mask id="background-only" maskUnits="userSpaceOnUse" x="0" y="0" width="2560" height="1440" style={{maskType:'luminance'}}>
     <rect width="2560" height="1440" fill="white"/>
     {[...spec.protectedPhotos,spec.protectedTitle].map((r,i)=><rect key={i} x={r.x} y={r.y} width={r.width} height={r.height} rx={r.radius} fill="black"/>)}
    </mask>
    <filter id="star-glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="5"/></filter>
   </defs>
   <g mask="url(#background-only)">
    {spec.dust.map((p,i)=>{const s=state(p);return <circle key={`dust-${i}`} cx={s.x} cy={s.y} r={p.radius} fill="#f2d38f" opacity={.22+.62*s.pulse}/>;})}
    {spec.stars.map((p,i)=>{const s=state(p);const scale=p.radius/33*(.5+.5*s.pulse**.5);return <g key={`star-${i}`} opacity={s.pulse**1.6} transform={`translate(${s.x} ${s.y}) rotate(${p.rotation+20*Math.sin(s.angle)}) scale(${scale})`}>
     <path d={starPath} fill="#dfad53" filter="url(#star-glow)"/>
     <path d={starPath} fill="#dfad53"/>
     <path d={starPath} fill="#fff5cf" transform="scale(.88)"/>
     <path d={starPath} fill="#fffffc" transform="scale(.67)"/>
     <circle r="3" fill="white"/>
    </g>;})}
   </g>
  </svg>
 </AbsoluteFill>;
};
export const CollageRoot: React.FC=()=> <Composition id="OppoGiftCollage19Sparkles" component={CollageSparkles} width={2560} height={1440} fps={60} durationInFrames={1800}/>;
registerRoot(CollageRoot);
