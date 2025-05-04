precision mediump float;
uniform vec2 u_resolution;

void main() {
    vec2 st = gl_FragCoord.xy / u_resolution.xy; // 正規化
    gl_FragColor = vec4(st, 0., 1.);
}