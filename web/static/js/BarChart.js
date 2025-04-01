var zh = Object.defineProperty;
var Hh = (e, t, n) => t in e ? zh(e, t, { enumerable: !0, configurable: !0, writable: !0, value: n }) : e[t] = n;
var Z = (e, t, n) => Hh(e, typeof t != "symbol" ? t + "" : t, n);
var tf = {};
/**
* @vue/shared v3.5.13
* (c) 2018-present Yuxi (Evan) You and Vue contributors
* @license MIT
**/
/*! #__NO_SIDE_EFFECTS__ */
// @__NO_SIDE_EFFECTS__
function Ye(e) {
  const t = /* @__PURE__ */ Object.create(null);
  for (const n of e.split(",")) t[n] = 1;
  return (n) => n in t;
}
const ut = tf.NODE_ENV !== "production" ? Object.freeze({}) : {}, Wn = tf.NODE_ENV !== "production" ? Object.freeze([]) : [], St = () => {
}, Wh = () => !1, Us = (e) => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && // uppercase letter
(e.charCodeAt(2) > 122 || e.charCodeAt(2) < 97), Ii = (e) => e.startsWith("onUpdate:"), _t = Object.assign, zr = (e, t) => {
  const n = e.indexOf(t);
  n > -1 && e.splice(n, 1);
}, Uh = Object.prototype.hasOwnProperty, at = (e, t) => Uh.call(e, t), U = Array.isArray, En = (e) => oo(e) === "[object Map]", ef = (e) => oo(e) === "[object Set]", K = (e) => typeof e == "function", bt = (e) => typeof e == "string", ln = (e) => typeof e == "symbol", dt = (e) => e !== null && typeof e == "object", Hr = (e) => (dt(e) || K(e)) && K(e.then) && K(e.catch), nf = Object.prototype.toString, oo = (e) => nf.call(e), Wr = (e) => oo(e).slice(8, -1), ro = (e) => oo(e) === "[object Object]", Ur = (e) => bt(e) && e !== "NaN" && e[0] !== "-" && "" + parseInt(e, 10) === e, Es = /* @__PURE__ */ Ye(
  // the leading comma is intentional so empty string "" is also included
  ",key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted"
), Yh = /* @__PURE__ */ Ye(
  "bind,cloak,else-if,else,for,html,if,model,on,once,pre,show,slot,text,memo"
), ao = (e) => {
  const t = /* @__PURE__ */ Object.create(null);
  return (n) => t[n] || (t[n] = e(n));
}, Kh = /-(\w)/g, Kt = ao(
  (e) => e.replace(Kh, (t, n) => n ? n.toUpperCase() : "")
), qh = /\B([A-Z])/g, Zt = ao(
  (e) => e.replace(qh, "-$1").toLowerCase()
), lo = ao((e) => e.charAt(0).toUpperCase() + e.slice(1)), bn = ao(
  (e) => e ? `on${lo(e)}` : ""
), On = (e, t) => !Object.is(e, t), ls = (e, ...t) => {
  for (let n = 0; n < e.length; n++)
    e[n](...t);
}, Li = (e, t, n, s = !1) => {
  Object.defineProperty(e, t, {
    configurable: !0,
    enumerable: !1,
    writable: s,
    value: n
  });
}, Xh = (e) => {
  const t = parseFloat(e);
  return isNaN(t) ? e : t;
}, Ra = (e) => {
  const t = bt(e) ? Number(e) : NaN;
  return isNaN(t) ? e : t;
};
let Ia;
const Ys = () => Ia || (Ia = typeof globalThis < "u" ? globalThis : typeof self < "u" ? self : typeof window < "u" ? window : typeof global < "u" ? global : {});
function co(e) {
  if (U(e)) {
    const t = {};
    for (let n = 0; n < e.length; n++) {
      const s = e[n], i = bt(s) ? Qh(s) : co(s);
      if (i)
        for (const o in i)
          t[o] = i[o];
    }
    return t;
  } else if (bt(e) || dt(e))
    return e;
}
const Gh = /;(?![^(]*\))/g, Zh = /:([^]+)/, Jh = /\/\*[^]*?\*\//g;
function Qh(e) {
  const t = {};
  return e.replace(Jh, "").split(Gh).forEach((n) => {
    if (n) {
      const s = n.split(Zh);
      s.length > 1 && (t[s[0].trim()] = s[1].trim());
    }
  }), t;
}
function Yr(e) {
  let t = "";
  if (bt(e))
    t = e;
  else if (U(e))
    for (let n = 0; n < e.length; n++) {
      const s = Yr(e[n]);
      s && (t += s + " ");
    }
  else if (dt(e))
    for (const n in e)
      e[n] && (t += n + " ");
  return t.trim();
}
const td = "html,body,base,head,link,meta,style,title,address,article,aside,footer,header,hgroup,h1,h2,h3,h4,h5,h6,nav,section,div,dd,dl,dt,figcaption,figure,picture,hr,img,li,main,ol,p,pre,ul,a,b,abbr,bdi,bdo,br,cite,code,data,dfn,em,i,kbd,mark,q,rp,rt,ruby,s,samp,small,span,strong,sub,sup,time,u,var,wbr,area,audio,map,track,video,embed,object,param,source,canvas,script,noscript,del,ins,caption,col,colgroup,table,thead,tbody,td,th,tr,button,datalist,fieldset,form,input,label,legend,meter,optgroup,option,output,progress,select,textarea,details,dialog,menu,summary,template,blockquote,iframe,tfoot", ed = "svg,animate,animateMotion,animateTransform,circle,clipPath,color-profile,defs,desc,discard,ellipse,feBlend,feColorMatrix,feComponentTransfer,feComposite,feConvolveMatrix,feDiffuseLighting,feDisplacementMap,feDistantLight,feDropShadow,feFlood,feFuncA,feFuncB,feFuncG,feFuncR,feGaussianBlur,feImage,feMerge,feMergeNode,feMorphology,feOffset,fePointLight,feSpecularLighting,feSpotLight,feTile,feTurbulence,filter,foreignObject,g,hatch,hatchpath,image,line,linearGradient,marker,mask,mesh,meshgradient,meshpatch,meshrow,metadata,mpath,path,pattern,polygon,polyline,radialGradient,rect,set,solidcolor,stop,switch,symbol,text,textPath,title,tspan,unknown,use,view", nd = "annotation,annotation-xml,maction,maligngroup,malignmark,math,menclose,merror,mfenced,mfrac,mfraction,mglyph,mi,mlabeledtr,mlongdiv,mmultiscripts,mn,mo,mover,mpadded,mphantom,mprescripts,mroot,mrow,ms,mscarries,mscarry,msgroup,msline,mspace,msqrt,msrow,mstack,mstyle,msub,msubsup,msup,mtable,mtd,mtext,mtr,munder,munderover,none,semantics", sd = /* @__PURE__ */ Ye(td), id = /* @__PURE__ */ Ye(ed), od = /* @__PURE__ */ Ye(nd), rd = "itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly", ad = /* @__PURE__ */ Ye(rd);
function sf(e) {
  return !!e || e === "";
}
const of = (e) => !!(e && e.__v_isRef === !0), ar = (e) => bt(e) ? e : e == null ? "" : U(e) || dt(e) && (e.toString === nf || !K(e.toString)) ? of(e) ? ar(e.value) : JSON.stringify(e, rf, 2) : String(e), rf = (e, t) => of(t) ? rf(e, t.value) : En(t) ? {
  [`Map(${t.size})`]: [...t.entries()].reduce(
    (n, [s, i], o) => (n[So(s, o) + " =>"] = i, n),
    {}
  )
} : ef(t) ? {
  [`Set(${t.size})`]: [...t.values()].map((n) => So(n))
} : ln(t) ? So(t) : dt(t) && !U(t) && !ro(t) ? String(t) : t, So = (e, t = "") => {
  var n;
  return (
    // Symbol.description in es2019+ so we need to cast here to pass
    // the lib: es2016 check
    ln(e) ? `Symbol(${(n = e.description) != null ? n : t})` : e
  );
};
var mt = {};
function Ae(e, ...t) {
  console.warn(`[Vue warn] ${e}`, ...t);
}
let Gt;
class ld {
  constructor(t = !1) {
    this.detached = t, this._active = !0, this.effects = [], this.cleanups = [], this._isPaused = !1, this.parent = Gt, !t && Gt && (this.index = (Gt.scopes || (Gt.scopes = [])).push(
      this
    ) - 1);
  }
  get active() {
    return this._active;
  }
  pause() {
    if (this._active) {
      this._isPaused = !0;
      let t, n;
      if (this.scopes)
        for (t = 0, n = this.scopes.length; t < n; t++)
          this.scopes[t].pause();
      for (t = 0, n = this.effects.length; t < n; t++)
        this.effects[t].pause();
    }
  }
  /**
   * Resumes the effect scope, including all child scopes and effects.
   */
  resume() {
    if (this._active && this._isPaused) {
      this._isPaused = !1;
      let t, n;
      if (this.scopes)
        for (t = 0, n = this.scopes.length; t < n; t++)
          this.scopes[t].resume();
      for (t = 0, n = this.effects.length; t < n; t++)
        this.effects[t].resume();
    }
  }
  run(t) {
    if (this._active) {
      const n = Gt;
      try {
        return Gt = this, t();
      } finally {
        Gt = n;
      }
    } else mt.NODE_ENV !== "production" && Ae("cannot run an inactive effect scope.");
  }
  /**
   * This should only be called on non-detached scopes
   * @internal
   */
  on() {
    Gt = this;
  }
  /**
   * This should only be called on non-detached scopes
   * @internal
   */
  off() {
    Gt = this.parent;
  }
  stop(t) {
    if (this._active) {
      this._active = !1;
      let n, s;
      for (n = 0, s = this.effects.length; n < s; n++)
        this.effects[n].stop();
      for (this.effects.length = 0, n = 0, s = this.cleanups.length; n < s; n++)
        this.cleanups[n]();
      if (this.cleanups.length = 0, this.scopes) {
        for (n = 0, s = this.scopes.length; n < s; n++)
          this.scopes[n].stop(!0);
        this.scopes.length = 0;
      }
      if (!this.detached && this.parent && !t) {
        const i = this.parent.scopes.pop();
        i && i !== this && (this.parent.scopes[this.index] = i, i.index = this.index);
      }
      this.parent = void 0;
    }
  }
}
function cd() {
  return Gt;
}
let lt;
const Mo = /* @__PURE__ */ new WeakSet();
class af {
  constructor(t) {
    this.fn = t, this.deps = void 0, this.depsTail = void 0, this.flags = 5, this.next = void 0, this.cleanup = void 0, this.scheduler = void 0, Gt && Gt.active && Gt.effects.push(this);
  }
  pause() {
    this.flags |= 64;
  }
  resume() {
    this.flags & 64 && (this.flags &= -65, Mo.has(this) && (Mo.delete(this), this.trigger()));
  }
  /**
   * @internal
   */
  notify() {
    this.flags & 2 && !(this.flags & 32) || this.flags & 8 || cf(this);
  }
  run() {
    if (!(this.flags & 1))
      return this.fn();
    this.flags |= 2, La(this), ff(this);
    const t = lt, n = de;
    lt = this, de = !0;
    try {
      return this.fn();
    } finally {
      mt.NODE_ENV !== "production" && lt !== this && Ae(
        "Active effect was not restored correctly - this is likely a Vue internal bug."
      ), uf(this), lt = t, de = n, this.flags &= -3;
    }
  }
  stop() {
    if (this.flags & 1) {
      for (let t = this.deps; t; t = t.nextDep)
        Xr(t);
      this.deps = this.depsTail = void 0, La(this), this.onStop && this.onStop(), this.flags &= -2;
    }
  }
  trigger() {
    this.flags & 64 ? Mo.add(this) : this.scheduler ? this.scheduler() : this.runIfDirty();
  }
  /**
   * @internal
   */
  runIfDirty() {
    lr(this) && this.run();
  }
  get dirty() {
    return lr(this);
  }
}
let lf = 0, Os, Ss;
function cf(e, t = !1) {
  if (e.flags |= 8, t) {
    e.next = Ss, Ss = e;
    return;
  }
  e.next = Os, Os = e;
}
function Kr() {
  lf++;
}
function qr() {
  if (--lf > 0)
    return;
  if (Ss) {
    let t = Ss;
    for (Ss = void 0; t; ) {
      const n = t.next;
      t.next = void 0, t.flags &= -9, t = n;
    }
  }
  let e;
  for (; Os; ) {
    let t = Os;
    for (Os = void 0; t; ) {
      const n = t.next;
      if (t.next = void 0, t.flags &= -9, t.flags & 1)
        try {
          t.trigger();
        } catch (s) {
          e || (e = s);
        }
      t = n;
    }
  }
  if (e) throw e;
}
function ff(e) {
  for (let t = e.deps; t; t = t.nextDep)
    t.version = -1, t.prevActiveLink = t.dep.activeLink, t.dep.activeLink = t;
}
function uf(e) {
  let t, n = e.depsTail, s = n;
  for (; s; ) {
    const i = s.prevDep;
    s.version === -1 ? (s === n && (n = i), Xr(s), fd(s)) : t = s, s.dep.activeLink = s.prevActiveLink, s.prevActiveLink = void 0, s = i;
  }
  e.deps = t, e.depsTail = n;
}
function lr(e) {
  for (let t = e.deps; t; t = t.nextDep)
    if (t.dep.version !== t.version || t.dep.computed && (hf(t.dep.computed) || t.dep.version !== t.version))
      return !0;
  return !!e._dirty;
}
function hf(e) {
  if (e.flags & 4 && !(e.flags & 16) || (e.flags &= -17, e.globalVersion === Rs))
    return;
  e.globalVersion = Rs;
  const t = e.dep;
  if (e.flags |= 2, t.version > 0 && !e.isSSR && e.deps && !lr(e)) {
    e.flags &= -3;
    return;
  }
  const n = lt, s = de;
  lt = e, de = !0;
  try {
    ff(e);
    const i = e.fn(e._value);
    (t.version === 0 || On(i, e._value)) && (e._value = i, t.version++);
  } catch (i) {
    throw t.version++, i;
  } finally {
    lt = n, de = s, uf(e), e.flags &= -3;
  }
}
function Xr(e, t = !1) {
  const { dep: n, prevSub: s, nextSub: i } = e;
  if (s && (s.nextSub = i, e.prevSub = void 0), i && (i.prevSub = s, e.nextSub = void 0), mt.NODE_ENV !== "production" && n.subsHead === e && (n.subsHead = i), n.subs === e && (n.subs = s, !s && n.computed)) {
    n.computed.flags &= -5;
    for (let o = n.computed.deps; o; o = o.nextDep)
      Xr(o, !0);
  }
  !t && !--n.sc && n.map && n.map.delete(n.key);
}
function fd(e) {
  const { prevDep: t, nextDep: n } = e;
  t && (t.nextDep = n, e.prevDep = void 0), n && (n.prevDep = t, e.nextDep = void 0);
}
let de = !0;
const df = [];
function Ke() {
  df.push(de), de = !1;
}
function qe() {
  const e = df.pop();
  de = e === void 0 ? !0 : e;
}
function La(e) {
  const { cleanup: t } = e;
  if (e.cleanup = void 0, t) {
    const n = lt;
    lt = void 0;
    try {
      t();
    } finally {
      lt = n;
    }
  }
}
let Rs = 0;
class ud {
  constructor(t, n) {
    this.sub = t, this.dep = n, this.version = n.version, this.nextDep = this.prevDep = this.nextSub = this.prevSub = this.prevActiveLink = void 0;
  }
}
class pf {
  constructor(t) {
    this.computed = t, this.version = 0, this.activeLink = void 0, this.subs = void 0, this.map = void 0, this.key = void 0, this.sc = 0, mt.NODE_ENV !== "production" && (this.subsHead = void 0);
  }
  track(t) {
    if (!lt || !de || lt === this.computed)
      return;
    let n = this.activeLink;
    if (n === void 0 || n.sub !== lt)
      n = this.activeLink = new ud(lt, this), lt.deps ? (n.prevDep = lt.depsTail, lt.depsTail.nextDep = n, lt.depsTail = n) : lt.deps = lt.depsTail = n, gf(n);
    else if (n.version === -1 && (n.version = this.version, n.nextDep)) {
      const s = n.nextDep;
      s.prevDep = n.prevDep, n.prevDep && (n.prevDep.nextDep = s), n.prevDep = lt.depsTail, n.nextDep = void 0, lt.depsTail.nextDep = n, lt.depsTail = n, lt.deps === n && (lt.deps = s);
    }
    return mt.NODE_ENV !== "production" && lt.onTrack && lt.onTrack(
      _t(
        {
          effect: lt
        },
        t
      )
    ), n;
  }
  trigger(t) {
    this.version++, Rs++, this.notify(t);
  }
  notify(t) {
    Kr();
    try {
      if (mt.NODE_ENV !== "production")
        for (let n = this.subsHead; n; n = n.nextSub)
          n.sub.onTrigger && !(n.sub.flags & 8) && n.sub.onTrigger(
            _t(
              {
                effect: n.sub
              },
              t
            )
          );
      for (let n = this.subs; n; n = n.prevSub)
        n.sub.notify() && n.sub.dep.notify();
    } finally {
      qr();
    }
  }
}
function gf(e) {
  if (e.dep.sc++, e.sub.flags & 4) {
    const t = e.dep.computed;
    if (t && !e.dep.subs) {
      t.flags |= 20;
      for (let s = t.deps; s; s = s.nextDep)
        gf(s);
    }
    const n = e.dep.subs;
    n !== e && (e.prevSub = n, n && (n.nextSub = e)), mt.NODE_ENV !== "production" && e.dep.subsHead === void 0 && (e.dep.subsHead = e), e.dep.subs = e;
  }
}
const cr = /* @__PURE__ */ new WeakMap(), Sn = Symbol(
  mt.NODE_ENV !== "production" ? "Object iterate" : ""
), fr = Symbol(
  mt.NODE_ENV !== "production" ? "Map keys iterate" : ""
), Is = Symbol(
  mt.NODE_ENV !== "production" ? "Array iterate" : ""
);
function Ot(e, t, n) {
  if (de && lt) {
    let s = cr.get(e);
    s || cr.set(e, s = /* @__PURE__ */ new Map());
    let i = s.get(n);
    i || (s.set(n, i = new pf()), i.map = s, i.key = n), mt.NODE_ENV !== "production" ? i.track({
      target: e,
      type: t,
      key: n
    }) : i.track();
  }
}
function Se(e, t, n, s, i, o) {
  const r = cr.get(e);
  if (!r) {
    Rs++;
    return;
  }
  const a = (l) => {
    l && (mt.NODE_ENV !== "production" ? l.trigger({
      target: e,
      type: t,
      key: n,
      newValue: s,
      oldValue: i,
      oldTarget: o
    }) : l.trigger());
  };
  if (Kr(), t === "clear")
    r.forEach(a);
  else {
    const l = U(e), c = l && Ur(n);
    if (l && n === "length") {
      const f = Number(s);
      r.forEach((u, h) => {
        (h === "length" || h === Is || !ln(h) && h >= f) && a(u);
      });
    } else
      switch ((n !== void 0 || r.has(void 0)) && a(r.get(n)), c && a(r.get(Is)), t) {
        case "add":
          l ? c && a(r.get("length")) : (a(r.get(Sn)), En(e) && a(r.get(fr)));
          break;
        case "delete":
          l || (a(r.get(Sn)), En(e) && a(r.get(fr)));
          break;
        case "set":
          En(e) && a(r.get(Sn));
          break;
      }
  }
  qr();
}
function In(e) {
  const t = et(e);
  return t === e ? t : (Ot(t, "iterate", Is), qt(e) ? t : t.map(Ut));
}
function fo(e) {
  return Ot(e = et(e), "iterate", Is), e;
}
const hd = {
  __proto__: null,
  [Symbol.iterator]() {
    return ko(this, Symbol.iterator, Ut);
  },
  concat(...e) {
    return In(this).concat(
      ...e.map((t) => U(t) ? In(t) : t)
    );
  },
  entries() {
    return ko(this, "entries", (e) => (e[1] = Ut(e[1]), e));
  },
  every(e, t) {
    return Ie(this, "every", e, t, void 0, arguments);
  },
  filter(e, t) {
    return Ie(this, "filter", e, t, (n) => n.map(Ut), arguments);
  },
  find(e, t) {
    return Ie(this, "find", e, t, Ut, arguments);
  },
  findIndex(e, t) {
    return Ie(this, "findIndex", e, t, void 0, arguments);
  },
  findLast(e, t) {
    return Ie(this, "findLast", e, t, Ut, arguments);
  },
  findLastIndex(e, t) {
    return Ie(this, "findLastIndex", e, t, void 0, arguments);
  },
  // flat, flatMap could benefit from ARRAY_ITERATE but are not straight-forward to implement
  forEach(e, t) {
    return Ie(this, "forEach", e, t, void 0, arguments);
  },
  includes(...e) {
    return No(this, "includes", e);
  },
  indexOf(...e) {
    return No(this, "indexOf", e);
  },
  join(e) {
    return In(this).join(e);
  },
  // keys() iterator only reads `length`, no optimisation required
  lastIndexOf(...e) {
    return No(this, "lastIndexOf", e);
  },
  map(e, t) {
    return Ie(this, "map", e, t, void 0, arguments);
  },
  pop() {
    return cs(this, "pop");
  },
  push(...e) {
    return cs(this, "push", e);
  },
  reduce(e, ...t) {
    return Fa(this, "reduce", e, t);
  },
  reduceRight(e, ...t) {
    return Fa(this, "reduceRight", e, t);
  },
  shift() {
    return cs(this, "shift");
  },
  // slice could use ARRAY_ITERATE but also seems to beg for range tracking
  some(e, t) {
    return Ie(this, "some", e, t, void 0, arguments);
  },
  splice(...e) {
    return cs(this, "splice", e);
  },
  toReversed() {
    return In(this).toReversed();
  },
  toSorted(e) {
    return In(this).toSorted(e);
  },
  toSpliced(...e) {
    return In(this).toSpliced(...e);
  },
  unshift(...e) {
    return cs(this, "unshift", e);
  },
  values() {
    return ko(this, "values", Ut);
  }
};
function ko(e, t, n) {
  const s = fo(e), i = s[t]();
  return s !== e && !qt(e) && (i._next = i.next, i.next = () => {
    const o = i._next();
    return o.value && (o.value = n(o.value)), o;
  }), i;
}
const dd = Array.prototype;
function Ie(e, t, n, s, i, o) {
  const r = fo(e), a = r !== e && !qt(e), l = r[t];
  if (l !== dd[t]) {
    const u = l.apply(e, o);
    return a ? Ut(u) : u;
  }
  let c = n;
  r !== e && (a ? c = function(u, h) {
    return n.call(this, Ut(u), h, e);
  } : n.length > 2 && (c = function(u, h) {
    return n.call(this, u, h, e);
  }));
  const f = l.call(r, c, s);
  return a && i ? i(f) : f;
}
function Fa(e, t, n, s) {
  const i = fo(e);
  let o = n;
  return i !== e && (qt(e) ? n.length > 3 && (o = function(r, a, l) {
    return n.call(this, r, a, l, e);
  }) : o = function(r, a, l) {
    return n.call(this, r, Ut(a), l, e);
  }), i[t](o, ...s);
}
function No(e, t, n) {
  const s = et(e);
  Ot(s, "iterate", Is);
  const i = s[t](...n);
  return (i === -1 || i === !1) && Fi(n[0]) ? (n[0] = et(n[0]), s[t](...n)) : i;
}
function cs(e, t, n = []) {
  Ke(), Kr();
  const s = et(e)[t].apply(e, n);
  return qr(), qe(), s;
}
const pd = /* @__PURE__ */ Ye("__proto__,__v_isRef,__isVue"), mf = new Set(
  /* @__PURE__ */ Object.getOwnPropertyNames(Symbol).filter((e) => e !== "arguments" && e !== "caller").map((e) => Symbol[e]).filter(ln)
);
function gd(e) {
  ln(e) || (e = String(e));
  const t = et(this);
  return Ot(t, "has", e), t.hasOwnProperty(e);
}
class bf {
  constructor(t = !1, n = !1) {
    this._isReadonly = t, this._isShallow = n;
  }
  get(t, n, s) {
    if (n === "__v_skip") return t.__v_skip;
    const i = this._isReadonly, o = this._isShallow;
    if (n === "__v_isReactive")
      return !i;
    if (n === "__v_isReadonly")
      return i;
    if (n === "__v_isShallow")
      return o;
    if (n === "__v_raw")
      return s === (i ? o ? Ef : wf : o ? vf : xf).get(t) || // receiver is not the reactive proxy, but has the same prototype
      // this means the receiver is a user proxy of the reactive proxy
      Object.getPrototypeOf(t) === Object.getPrototypeOf(s) ? t : void 0;
    const r = U(t);
    if (!i) {
      let l;
      if (r && (l = hd[n]))
        return l;
      if (n === "hasOwnProperty")
        return gd;
    }
    const a = Reflect.get(
      t,
      n,
      // if this is a proxy wrapping a ref, return methods using the raw ref
      // as receiver so that we don't have to call `toRaw` on the ref in all
      // its class methods
      kt(t) ? t : s
    );
    return (ln(n) ? mf.has(n) : pd(n)) || (i || Ot(t, "get", n), o) ? a : kt(a) ? r && Ur(n) ? a : a.value : dt(a) ? i ? Of(a) : Gr(a) : a;
  }
}
class _f extends bf {
  constructor(t = !1) {
    super(!1, t);
  }
  set(t, n, s, i) {
    let o = t[n];
    if (!this._isShallow) {
      const l = sn(o);
      if (!qt(s) && !sn(s) && (o = et(o), s = et(s)), !U(t) && kt(o) && !kt(s))
        return l ? !1 : (o.value = s, !0);
    }
    const r = U(t) && Ur(n) ? Number(n) < t.length : at(t, n), a = Reflect.set(
      t,
      n,
      s,
      kt(t) ? t : i
    );
    return t === et(i) && (r ? On(s, o) && Se(t, "set", n, s, o) : Se(t, "add", n, s)), a;
  }
  deleteProperty(t, n) {
    const s = at(t, n), i = t[n], o = Reflect.deleteProperty(t, n);
    return o && s && Se(t, "delete", n, void 0, i), o;
  }
  has(t, n) {
    const s = Reflect.has(t, n);
    return (!ln(n) || !mf.has(n)) && Ot(t, "has", n), s;
  }
  ownKeys(t) {
    return Ot(
      t,
      "iterate",
      U(t) ? "length" : Sn
    ), Reflect.ownKeys(t);
  }
}
class yf extends bf {
  constructor(t = !1) {
    super(!0, t);
  }
  set(t, n) {
    return mt.NODE_ENV !== "production" && Ae(
      `Set operation on key "${String(n)}" failed: target is readonly.`,
      t
    ), !0;
  }
  deleteProperty(t, n) {
    return mt.NODE_ENV !== "production" && Ae(
      `Delete operation on key "${String(n)}" failed: target is readonly.`,
      t
    ), !0;
  }
}
const md = /* @__PURE__ */ new _f(), bd = /* @__PURE__ */ new yf(), _d = /* @__PURE__ */ new _f(!0), yd = /* @__PURE__ */ new yf(!0), ur = (e) => e, Qs = (e) => Reflect.getPrototypeOf(e);
function xd(e, t, n) {
  return function(...s) {
    const i = this.__v_raw, o = et(i), r = En(o), a = e === "entries" || e === Symbol.iterator && r, l = e === "keys" && r, c = i[e](...s), f = n ? ur : t ? hr : Ut;
    return !t && Ot(
      o,
      "iterate",
      l ? fr : Sn
    ), {
      // iterator protocol
      next() {
        const { value: u, done: h } = c.next();
        return h ? { value: u, done: h } : {
          value: a ? [f(u[0]), f(u[1])] : f(u),
          done: h
        };
      },
      // iterable protocol
      [Symbol.iterator]() {
        return this;
      }
    };
  };
}
function ti(e) {
  return function(...t) {
    if (mt.NODE_ENV !== "production") {
      const n = t[0] ? `on key "${t[0]}" ` : "";
      Ae(
        `${lo(e)} operation ${n}failed: target is readonly.`,
        et(this)
      );
    }
    return e === "delete" ? !1 : e === "clear" ? void 0 : this;
  };
}
function vd(e, t) {
  const n = {
    get(i) {
      const o = this.__v_raw, r = et(o), a = et(i);
      e || (On(i, a) && Ot(r, "get", i), Ot(r, "get", a));
      const { has: l } = Qs(r), c = t ? ur : e ? hr : Ut;
      if (l.call(r, i))
        return c(o.get(i));
      if (l.call(r, a))
        return c(o.get(a));
      o !== r && o.get(i);
    },
    get size() {
      const i = this.__v_raw;
      return !e && Ot(et(i), "iterate", Sn), Reflect.get(i, "size", i);
    },
    has(i) {
      const o = this.__v_raw, r = et(o), a = et(i);
      return e || (On(i, a) && Ot(r, "has", i), Ot(r, "has", a)), i === a ? o.has(i) : o.has(i) || o.has(a);
    },
    forEach(i, o) {
      const r = this, a = r.__v_raw, l = et(a), c = t ? ur : e ? hr : Ut;
      return !e && Ot(l, "iterate", Sn), a.forEach((f, u) => i.call(o, c(f), c(u), r));
    }
  };
  return _t(
    n,
    e ? {
      add: ti("add"),
      set: ti("set"),
      delete: ti("delete"),
      clear: ti("clear")
    } : {
      add(i) {
        !t && !qt(i) && !sn(i) && (i = et(i));
        const o = et(this);
        return Qs(o).has.call(o, i) || (o.add(i), Se(o, "add", i, i)), this;
      },
      set(i, o) {
        !t && !qt(o) && !sn(o) && (o = et(o));
        const r = et(this), { has: a, get: l } = Qs(r);
        let c = a.call(r, i);
        c ? mt.NODE_ENV !== "production" && $a(r, a, i) : (i = et(i), c = a.call(r, i));
        const f = l.call(r, i);
        return r.set(i, o), c ? On(o, f) && Se(r, "set", i, o, f) : Se(r, "add", i, o), this;
      },
      delete(i) {
        const o = et(this), { has: r, get: a } = Qs(o);
        let l = r.call(o, i);
        l ? mt.NODE_ENV !== "production" && $a(o, r, i) : (i = et(i), l = r.call(o, i));
        const c = a ? a.call(o, i) : void 0, f = o.delete(i);
        return l && Se(o, "delete", i, void 0, c), f;
      },
      clear() {
        const i = et(this), o = i.size !== 0, r = mt.NODE_ENV !== "production" ? En(i) ? new Map(i) : new Set(i) : void 0, a = i.clear();
        return o && Se(
          i,
          "clear",
          void 0,
          void 0,
          r
        ), a;
      }
    }
  ), [
    "keys",
    "values",
    "entries",
    Symbol.iterator
  ].forEach((i) => {
    n[i] = xd(i, e, t);
  }), n;
}
function uo(e, t) {
  const n = vd(e, t);
  return (s, i, o) => i === "__v_isReactive" ? !e : i === "__v_isReadonly" ? e : i === "__v_raw" ? s : Reflect.get(
    at(n, i) && i in s ? n : s,
    i,
    o
  );
}
const wd = {
  get: /* @__PURE__ */ uo(!1, !1)
}, Ed = {
  get: /* @__PURE__ */ uo(!1, !0)
}, Od = {
  get: /* @__PURE__ */ uo(!0, !1)
}, Sd = {
  get: /* @__PURE__ */ uo(!0, !0)
};
function $a(e, t, n) {
  const s = et(n);
  if (s !== n && t.call(e, s)) {
    const i = Wr(e);
    Ae(
      `Reactive ${i} contains both the raw and reactive versions of the same object${i === "Map" ? " as keys" : ""}, which can lead to inconsistencies. Avoid differentiating between the raw and reactive versions of an object and only use the reactive version if possible.`
    );
  }
}
const xf = /* @__PURE__ */ new WeakMap(), vf = /* @__PURE__ */ new WeakMap(), wf = /* @__PURE__ */ new WeakMap(), Ef = /* @__PURE__ */ new WeakMap();
function Md(e) {
  switch (e) {
    case "Object":
    case "Array":
      return 1;
    case "Map":
    case "Set":
    case "WeakMap":
    case "WeakSet":
      return 2;
    default:
      return 0;
  }
}
function kd(e) {
  return e.__v_skip || !Object.isExtensible(e) ? 0 : Md(Wr(e));
}
function Gr(e) {
  return sn(e) ? e : ho(
    e,
    !1,
    md,
    wd,
    xf
  );
}
function Nd(e) {
  return ho(
    e,
    !1,
    _d,
    Ed,
    vf
  );
}
function Of(e) {
  return ho(
    e,
    !0,
    bd,
    Od,
    wf
  );
}
function ke(e) {
  return ho(
    e,
    !0,
    yd,
    Sd,
    Ef
  );
}
function ho(e, t, n, s, i) {
  if (!dt(e))
    return mt.NODE_ENV !== "production" && Ae(
      `value cannot be made ${t ? "readonly" : "reactive"}: ${String(
        e
      )}`
    ), e;
  if (e.__v_raw && !(t && e.__v_isReactive))
    return e;
  const o = i.get(e);
  if (o)
    return o;
  const r = kd(e);
  if (r === 0)
    return e;
  const a = new Proxy(
    e,
    r === 2 ? s : n
  );
  return i.set(e, a), a;
}
function Mn(e) {
  return sn(e) ? Mn(e.__v_raw) : !!(e && e.__v_isReactive);
}
function sn(e) {
  return !!(e && e.__v_isReadonly);
}
function qt(e) {
  return !!(e && e.__v_isShallow);
}
function Fi(e) {
  return e ? !!e.__v_raw : !1;
}
function et(e) {
  const t = e && e.__v_raw;
  return t ? et(t) : e;
}
function Dd(e) {
  return !at(e, "__v_skip") && Object.isExtensible(e) && Li(e, "__v_skip", !0), e;
}
const Ut = (e) => dt(e) ? Gr(e) : e, hr = (e) => dt(e) ? Of(e) : e;
function kt(e) {
  return e ? e.__v_isRef === !0 : !1;
}
function Sf(e) {
  return kt(e) ? e.value : e;
}
const Cd = {
  get: (e, t, n) => t === "__v_raw" ? e : Sf(Reflect.get(e, t, n)),
  set: (e, t, n, s) => {
    const i = e[t];
    return kt(i) && !kt(n) ? (i.value = n, !0) : Reflect.set(e, t, n, s);
  }
};
function Mf(e) {
  return Mn(e) ? e : new Proxy(e, Cd);
}
class Pd {
  constructor(t, n, s) {
    this.fn = t, this.setter = n, this._value = void 0, this.dep = new pf(this), this.__v_isRef = !0, this.deps = void 0, this.depsTail = void 0, this.flags = 16, this.globalVersion = Rs - 1, this.next = void 0, this.effect = this, this.__v_isReadonly = !n, this.isSSR = s;
  }
  /**
   * @internal
   */
  notify() {
    if (this.flags |= 16, !(this.flags & 8) && // avoid infinite self recursion
    lt !== this)
      return cf(this, !0), !0;
  }
  get value() {
    const t = mt.NODE_ENV !== "production" ? this.dep.track({
      target: this,
      type: "get",
      key: "value"
    }) : this.dep.track();
    return hf(this), t && (t.version = this.dep.version), this._value;
  }
  set value(t) {
    this.setter ? this.setter(t) : mt.NODE_ENV !== "production" && Ae("Write operation failed: computed value is readonly");
  }
}
function Td(e, t, n = !1) {
  let s, i;
  return K(e) ? s = e : (s = e.get, i = e.set), new Pd(s, i, n);
}
const ei = {}, $i = /* @__PURE__ */ new WeakMap();
let _n;
function Ad(e, t = !1, n = _n) {
  if (n) {
    let s = $i.get(n);
    s || $i.set(n, s = []), s.push(e);
  } else mt.NODE_ENV !== "production" && !t && Ae(
    "onWatcherCleanup() was called when there was no active watcher to associate with."
  );
}
function Vd(e, t, n = ut) {
  const { immediate: s, deep: i, once: o, scheduler: r, augmentJob: a, call: l } = n, c = (w) => {
    (n.onWarn || Ae)(
      "Invalid watch source: ",
      w,
      "A watch source can only be a getter/effect function, a ref, a reactive object, or an array of these types."
    );
  }, f = (w) => i ? w : qt(w) || i === !1 || i === 0 ? Je(w, 1) : Je(w);
  let u, h, d, p, g = !1, b = !1;
  if (kt(e) ? (h = () => e.value, g = qt(e)) : Mn(e) ? (h = () => f(e), g = !0) : U(e) ? (b = !0, g = e.some((w) => Mn(w) || qt(w)), h = () => e.map((w) => {
    if (kt(w))
      return w.value;
    if (Mn(w))
      return f(w);
    if (K(w))
      return l ? l(w, 2) : w();
    mt.NODE_ENV !== "production" && c(w);
  })) : K(e) ? t ? h = l ? () => l(e, 2) : e : h = () => {
    if (d) {
      Ke();
      try {
        d();
      } finally {
        qe();
      }
    }
    const w = _n;
    _n = u;
    try {
      return l ? l(e, 3, [p]) : e(p);
    } finally {
      _n = w;
    }
  } : (h = St, mt.NODE_ENV !== "production" && c(e)), t && i) {
    const w = h, k = i === !0 ? 1 / 0 : i;
    h = () => Je(w(), k);
  }
  const y = cd(), O = () => {
    u.stop(), y && y.active && zr(y.effects, u);
  };
  if (o && t) {
    const w = t;
    t = (...k) => {
      w(...k), O();
    };
  }
  let M = b ? new Array(e.length).fill(ei) : ei;
  const P = (w) => {
    if (!(!(u.flags & 1) || !u.dirty && !w))
      if (t) {
        const k = u.run();
        if (i || g || (b ? k.some((v, S) => On(v, M[S])) : On(k, M))) {
          d && d();
          const v = _n;
          _n = u;
          try {
            const S = [
              k,
              // pass undefined as the old value when it's changed for the first time
              M === ei ? void 0 : b && M[0] === ei ? [] : M,
              p
            ];
            l ? l(t, 3, S) : (
              // @ts-expect-error
              t(...S)
            ), M = k;
          } finally {
            _n = v;
          }
        }
      } else
        u.run();
  };
  return a && a(P), u = new af(h), u.scheduler = r ? () => r(P, !1) : P, p = (w) => Ad(w, !1, u), d = u.onStop = () => {
    const w = $i.get(u);
    if (w) {
      if (l)
        l(w, 4);
      else
        for (const k of w) k();
      $i.delete(u);
    }
  }, mt.NODE_ENV !== "production" && (u.onTrack = n.onTrack, u.onTrigger = n.onTrigger), t ? s ? P(!0) : M = u.run() : r ? r(P.bind(null, !0), !0) : u.run(), O.pause = u.pause.bind(u), O.resume = u.resume.bind(u), O.stop = O, O;
}
function Je(e, t = 1 / 0, n) {
  if (t <= 0 || !dt(e) || e.__v_skip || (n = n || /* @__PURE__ */ new Set(), n.has(e)))
    return e;
  if (n.add(e), t--, kt(e))
    Je(e.value, t, n);
  else if (U(e))
    for (let s = 0; s < e.length; s++)
      Je(e[s], t, n);
  else if (ef(e) || En(e))
    e.forEach((s) => {
      Je(s, t, n);
    });
  else if (ro(e)) {
    for (const s in e)
      Je(e[s], t, n);
    for (const s of Object.getOwnPropertySymbols(e))
      Object.prototype.propertyIsEnumerable.call(e, s) && Je(e[s], t, n);
  }
  return e;
}
var x = {};
const kn = [];
function Ei(e) {
  kn.push(e);
}
function Oi() {
  kn.pop();
}
let Do = !1;
function R(e, ...t) {
  if (Do) return;
  Do = !0, Ke();
  const n = kn.length ? kn[kn.length - 1].component : null, s = n && n.appContext.config.warnHandler, i = Rd();
  if (s)
    Jn(
      s,
      n,
      11,
      [
        // eslint-disable-next-line no-restricted-syntax
        e + t.map((o) => {
          var r, a;
          return (a = (r = o.toString) == null ? void 0 : r.call(o)) != null ? a : JSON.stringify(o);
        }).join(""),
        n && n.proxy,
        i.map(
          ({ vnode: o }) => `at <${_o(n, o.type)}>`
        ).join(`
`),
        i
      ]
    );
  else {
    const o = [`[Vue warn]: ${e}`, ...t];
    i.length && o.push(`
`, ...Id(i)), console.warn(...o);
  }
  qe(), Do = !1;
}
function Rd() {
  let e = kn[kn.length - 1];
  if (!e)
    return [];
  const t = [];
  for (; e; ) {
    const n = t[0];
    n && n.vnode === e ? n.recurseCount++ : t.push({
      vnode: e,
      recurseCount: 0
    });
    const s = e.component && e.component.parent;
    e = s && s.vnode;
  }
  return t;
}
function Id(e) {
  const t = [];
  return e.forEach((n, s) => {
    t.push(...s === 0 ? [] : [`
`], ...Ld(n));
  }), t;
}
function Ld({ vnode: e, recurseCount: t }) {
  const n = t > 0 ? `... (${t} recursive calls)` : "", s = e.component ? e.component.parent == null : !1, i = ` at <${_o(
    e.component,
    e.type,
    s
  )}`, o = ">" + n;
  return e.props ? [i, ...Fd(e.props), o] : [i + o];
}
function Fd(e) {
  const t = [], n = Object.keys(e);
  return n.slice(0, 3).forEach((s) => {
    t.push(...kf(s, e[s]));
  }), n.length > 3 && t.push(" ..."), t;
}
function kf(e, t, n) {
  return bt(t) ? (t = JSON.stringify(t), n ? t : [`${e}=${t}`]) : typeof t == "number" || typeof t == "boolean" || t == null ? n ? t : [`${e}=${t}`] : kt(t) ? (t = kf(e, et(t.value), !0), n ? t : [`${e}=Ref<`, t, ">"]) : K(t) ? [`${e}=fn${t.name ? `<${t.name}>` : ""}`] : (t = et(t), n ? t : [`${e}=`, t]);
}
const Zr = {
  sp: "serverPrefetch hook",
  bc: "beforeCreate hook",
  c: "created hook",
  bm: "beforeMount hook",
  m: "mounted hook",
  bu: "beforeUpdate hook",
  u: "updated",
  bum: "beforeUnmount hook",
  um: "unmounted hook",
  a: "activated hook",
  da: "deactivated hook",
  ec: "errorCaptured hook",
  rtc: "renderTracked hook",
  rtg: "renderTriggered hook",
  0: "setup function",
  1: "render function",
  2: "watcher getter",
  3: "watcher callback",
  4: "watcher cleanup function",
  5: "native event handler",
  6: "component event handler",
  7: "vnode hook",
  8: "directive hook",
  9: "transition hook",
  10: "app errorHandler",
  11: "app warnHandler",
  12: "ref function",
  13: "async component loader",
  14: "scheduler flush",
  15: "component update",
  16: "app unmount cleanup function"
};
function Jn(e, t, n, s) {
  try {
    return s ? e(...s) : e();
  } catch (i) {
    Ks(i, t, n);
  }
}
function Ve(e, t, n, s) {
  if (K(e)) {
    const i = Jn(e, t, n, s);
    return i && Hr(i) && i.catch((o) => {
      Ks(o, t, n);
    }), i;
  }
  if (U(e)) {
    const i = [];
    for (let o = 0; o < e.length; o++)
      i.push(Ve(e[o], t, n, s));
    return i;
  } else x.NODE_ENV !== "production" && R(
    `Invalid value type passed to callWithAsyncErrorHandling(): ${typeof e}`
  );
}
function Ks(e, t, n, s = !0) {
  const i = t ? t.vnode : null, { errorHandler: o, throwUnhandledErrorInProduction: r } = t && t.appContext.config || ut;
  if (t) {
    let a = t.parent;
    const l = t.proxy, c = x.NODE_ENV !== "production" ? Zr[n] : `https://vuejs.org/error-reference/#runtime-${n}`;
    for (; a; ) {
      const f = a.ec;
      if (f) {
        for (let u = 0; u < f.length; u++)
          if (f[u](e, l, c) === !1)
            return;
      }
      a = a.parent;
    }
    if (o) {
      Ke(), Jn(o, null, 10, [
        e,
        l,
        c
      ]), qe();
      return;
    }
  }
  $d(e, n, i, s, r);
}
function $d(e, t, n, s = !0, i = !1) {
  if (x.NODE_ENV !== "production") {
    const o = Zr[t];
    if (n && Ei(n), R(`Unhandled error${o ? ` during execution of ${o}` : ""}`), n && Oi(), s)
      throw e;
    console.error(e);
  } else {
    if (i)
      throw e;
    console.error(e);
  }
}
const jt = [];
let we = -1;
const Un = [];
let Ge = null, Hn = 0;
const Nf = /* @__PURE__ */ Promise.resolve();
let Bi = null;
const Bd = 100;
function Df(e) {
  const t = Bi || Nf;
  return e ? t.then(this ? e.bind(this) : e) : t;
}
function jd(e) {
  let t = we + 1, n = jt.length;
  for (; t < n; ) {
    const s = t + n >>> 1, i = jt[s], o = Ls(i);
    o < e || o === e && i.flags & 2 ? t = s + 1 : n = s;
  }
  return t;
}
function po(e) {
  if (!(e.flags & 1)) {
    const t = Ls(e), n = jt[jt.length - 1];
    !n || // fast path when the job id is larger than the tail
    !(e.flags & 2) && t >= Ls(n) ? jt.push(e) : jt.splice(jd(t), 0, e), e.flags |= 1, Cf();
  }
}
function Cf() {
  Bi || (Bi = Nf.then(Af));
}
function Pf(e) {
  U(e) ? Un.push(...e) : Ge && e.id === -1 ? Ge.splice(Hn + 1, 0, e) : e.flags & 1 || (Un.push(e), e.flags |= 1), Cf();
}
function Ba(e, t, n = we + 1) {
  for (x.NODE_ENV !== "production" && (t = t || /* @__PURE__ */ new Map()); n < jt.length; n++) {
    const s = jt[n];
    if (s && s.flags & 2) {
      if (e && s.id !== e.uid || x.NODE_ENV !== "production" && Jr(t, s))
        continue;
      jt.splice(n, 1), n--, s.flags & 4 && (s.flags &= -2), s(), s.flags & 4 || (s.flags &= -2);
    }
  }
}
function Tf(e) {
  if (Un.length) {
    const t = [...new Set(Un)].sort(
      (n, s) => Ls(n) - Ls(s)
    );
    if (Un.length = 0, Ge) {
      Ge.push(...t);
      return;
    }
    for (Ge = t, x.NODE_ENV !== "production" && (e = e || /* @__PURE__ */ new Map()), Hn = 0; Hn < Ge.length; Hn++) {
      const n = Ge[Hn];
      x.NODE_ENV !== "production" && Jr(e, n) || (n.flags & 4 && (n.flags &= -2), n.flags & 8 || n(), n.flags &= -2);
    }
    Ge = null, Hn = 0;
  }
}
const Ls = (e) => e.id == null ? e.flags & 2 ? -1 : 1 / 0 : e.id;
function Af(e) {
  x.NODE_ENV !== "production" && (e = e || /* @__PURE__ */ new Map());
  const t = x.NODE_ENV !== "production" ? (n) => Jr(e, n) : St;
  try {
    for (we = 0; we < jt.length; we++) {
      const n = jt[we];
      if (n && !(n.flags & 8)) {
        if (x.NODE_ENV !== "production" && t(n))
          continue;
        n.flags & 4 && (n.flags &= -2), Jn(
          n,
          n.i,
          n.i ? 15 : 14
        ), n.flags & 4 || (n.flags &= -2);
      }
    }
  } finally {
    for (; we < jt.length; we++) {
      const n = jt[we];
      n && (n.flags &= -2);
    }
    we = -1, jt.length = 0, Tf(e), Bi = null, (jt.length || Un.length) && Af(e);
  }
}
function Jr(e, t) {
  const n = e.get(t) || 0;
  if (n > Bd) {
    const s = t.i, i = s && _u(s.type);
    return Ks(
      `Maximum recursive updates exceeded${i ? ` in component <${i}>` : ""}. This means you have a reactive effect that is mutating its own dependencies and thus recursively triggering itself. Possible sources include component template, render function, updated hook or watcher source function.`,
      null,
      10
    ), !0;
  }
  return e.set(t, n + 1), !1;
}
let fe = !1;
const Si = /* @__PURE__ */ new Map();
x.NODE_ENV !== "production" && (Ys().__VUE_HMR_RUNTIME__ = {
  createRecord: Co(Vf),
  rerender: Co(Wd),
  reload: Co(Ud)
});
const Tn = /* @__PURE__ */ new Map();
function zd(e) {
  const t = e.type.__hmrId;
  let n = Tn.get(t);
  n || (Vf(t, e.type), n = Tn.get(t)), n.instances.add(e);
}
function Hd(e) {
  Tn.get(e.type.__hmrId).instances.delete(e);
}
function Vf(e, t) {
  return Tn.has(e) ? !1 : (Tn.set(e, {
    initialDef: ji(t),
    instances: /* @__PURE__ */ new Set()
  }), !0);
}
function ji(e) {
  return yu(e) ? e.__vccOpts : e;
}
function Wd(e, t) {
  const n = Tn.get(e);
  n && (n.initialDef.render = t, [...n.instances].forEach((s) => {
    t && (s.render = t, ji(s.type).render = t), s.renderCache = [], fe = !0, s.update(), fe = !1;
  }));
}
function Ud(e, t) {
  const n = Tn.get(e);
  if (!n) return;
  t = ji(t), ja(n.initialDef, t);
  const s = [...n.instances];
  for (let i = 0; i < s.length; i++) {
    const o = s[i], r = ji(o.type);
    let a = Si.get(r);
    a || (r !== n.initialDef && ja(r, t), Si.set(r, a = /* @__PURE__ */ new Set())), a.add(o), o.appContext.propsCache.delete(o.type), o.appContext.emitsCache.delete(o.type), o.appContext.optionsCache.delete(o.type), o.ceReload ? (a.add(o), o.ceReload(t.styles), a.delete(o)) : o.parent ? po(() => {
      fe = !0, o.parent.update(), fe = !1, a.delete(o);
    }) : o.appContext.reload ? o.appContext.reload() : typeof window < "u" ? window.location.reload() : console.warn(
      "[HMR] Root or manually mounted instance modified. Full reload required."
    ), o.root.ce && o !== o.root && o.root.ce._removeChildStyle(r);
  }
  Pf(() => {
    Si.clear();
  });
}
function ja(e, t) {
  _t(e, t);
  for (const n in e)
    n !== "__file" && !(n in t) && delete e[n];
}
function Co(e) {
  return (t, n) => {
    try {
      return e(t, n);
    } catch (s) {
      console.error(s), console.warn(
        "[HMR] Something went wrong during Vue component hot-reload. Full reload required."
      );
    }
  };
}
let Me, bs = [], dr = !1;
function qs(e, ...t) {
  Me ? Me.emit(e, ...t) : dr || bs.push({ event: e, args: t });
}
function Rf(e, t) {
  var n, s;
  Me = e, Me ? (Me.enabled = !0, bs.forEach(({ event: i, args: o }) => Me.emit(i, ...o)), bs = []) : /* handle late devtools injection - only do this if we are in an actual */ /* browser environment to avoid the timer handle stalling test runner exit */ /* (#4815) */ typeof window < "u" && // some envs mock window but not fully
  window.HTMLElement && // also exclude jsdom
  // eslint-disable-next-line no-restricted-syntax
  !((s = (n = window.navigator) == null ? void 0 : n.userAgent) != null && s.includes("jsdom")) ? ((t.__VUE_DEVTOOLS_HOOK_REPLAY__ = t.__VUE_DEVTOOLS_HOOK_REPLAY__ || []).push((o) => {
    Rf(o, t);
  }), setTimeout(() => {
    Me || (t.__VUE_DEVTOOLS_HOOK_REPLAY__ = null, dr = !0, bs = []);
  }, 3e3)) : (dr = !0, bs = []);
}
function Yd(e, t) {
  qs("app:init", e, t, {
    Fragment: le,
    Text: Xs,
    Comment: te,
    Static: Ni
  });
}
function Kd(e) {
  qs("app:unmount", e);
}
const qd = /* @__PURE__ */ Qr(
  "component:added"
  /* COMPONENT_ADDED */
), If = /* @__PURE__ */ Qr(
  "component:updated"
  /* COMPONENT_UPDATED */
), Xd = /* @__PURE__ */ Qr(
  "component:removed"
  /* COMPONENT_REMOVED */
), Gd = (e) => {
  Me && typeof Me.cleanupBuffer == "function" && // remove the component if it wasn't buffered
  !Me.cleanupBuffer(e) && Xd(e);
};
/*! #__NO_SIDE_EFFECTS__ */
// @__NO_SIDE_EFFECTS__
function Qr(e) {
  return (t) => {
    qs(
      e,
      t.appContext.app,
      t.uid,
      t.parent ? t.parent.uid : void 0,
      t
    );
  };
}
const Zd = /* @__PURE__ */ Lf(
  "perf:start"
  /* PERFORMANCE_START */
), Jd = /* @__PURE__ */ Lf(
  "perf:end"
  /* PERFORMANCE_END */
);
function Lf(e) {
  return (t, n, s) => {
    qs(e, t.appContext.app, t.uid, t, n, s);
  };
}
function Qd(e, t, n) {
  qs(
    "component:emit",
    e.appContext.app,
    e,
    t,
    n
  );
}
let Jt = null, Ff = null;
function zi(e) {
  const t = Jt;
  return Jt = e, Ff = e && e.type.__scopeId || null, t;
}
function tp(e, t = Jt, n) {
  if (!t || e._n)
    return e;
  const s = (...i) => {
    s._d && nl(-1);
    const o = zi(t);
    let r;
    try {
      r = e(...i);
    } finally {
      zi(o), s._d && nl(1);
    }
    return x.NODE_ENV !== "production" && If(t), r;
  };
  return s._n = !0, s._c = !0, s._d = !0, s;
}
function $f(e) {
  Yh(e) && R("Do not use built-in directive ids as custom directive id: " + e);
}
function hn(e, t, n, s) {
  const i = e.dirs, o = t && t.dirs;
  for (let r = 0; r < i.length; r++) {
    const a = i[r];
    o && (a.oldValue = o[r].value);
    let l = a.dir[s];
    l && (Ke(), Ve(l, n, 8, [
      e.el,
      a,
      e,
      t
    ]), qe());
  }
}
const Bf = Symbol("_vte"), ep = (e) => e.__isTeleport, Nn = (e) => e && (e.disabled || e.disabled === ""), za = (e) => e && (e.defer || e.defer === ""), Ha = (e) => typeof SVGElement < "u" && e instanceof SVGElement, Wa = (e) => typeof MathMLElement == "function" && e instanceof MathMLElement, pr = (e, t) => {
  const n = e && e.to;
  if (bt(n))
    if (t) {
      const s = t(n);
      return x.NODE_ENV !== "production" && !s && !Nn(e) && R(
        `Failed to locate Teleport target with selector "${n}". Note the target element must exist before the component is mounted - i.e. the target cannot be rendered by the component itself, and ideally should be outside of the entire Vue component tree.`
      ), s;
    } else
      return x.NODE_ENV !== "production" && R(
        "Current renderer does not support string target for Teleports. (missing querySelector renderer option)"
      ), null;
  else
    return x.NODE_ENV !== "production" && !n && !Nn(e) && R(`Invalid Teleport target: ${n}`), n;
}, jf = {
  name: "Teleport",
  __isTeleport: !0,
  process(e, t, n, s, i, o, r, a, l, c) {
    const {
      mc: f,
      pc: u,
      pbc: h,
      o: { insert: d, querySelector: p, createText: g, createComment: b }
    } = c, y = Nn(t.props);
    let { shapeFlag: O, children: M, dynamicChildren: P } = t;
    if (x.NODE_ENV !== "production" && fe && (l = !1, P = null), e == null) {
      const w = t.el = x.NODE_ENV !== "production" ? b("teleport start") : g(""), k = t.anchor = x.NODE_ENV !== "production" ? b("teleport end") : g("");
      d(w, n, s), d(k, n, s);
      const v = (D, F) => {
        O & 16 && (i && i.isCE && (i.ce._teleportTarget = D), f(
          M,
          D,
          F,
          i,
          o,
          r,
          a,
          l
        ));
      }, S = () => {
        const D = t.target = pr(t.props, p), F = zf(D, t, g, d);
        D ? (r !== "svg" && Ha(D) ? r = "svg" : r !== "mathml" && Wa(D) && (r = "mathml"), y || (v(D, F), Mi(t, !1))) : x.NODE_ENV !== "production" && !y && R(
          "Invalid Teleport target on mount:",
          D,
          `(${typeof D})`
        );
      };
      y && (v(n, k), Mi(t, !0)), za(t.props) ? Bt(() => {
        S(), t.el.__isMounted = !0;
      }, o) : S();
    } else {
      if (za(t.props) && !e.el.__isMounted) {
        Bt(() => {
          jf.process(
            e,
            t,
            n,
            s,
            i,
            o,
            r,
            a,
            l,
            c
          ), delete e.el.__isMounted;
        }, o);
        return;
      }
      t.el = e.el, t.targetStart = e.targetStart;
      const w = t.anchor = e.anchor, k = t.target = e.target, v = t.targetAnchor = e.targetAnchor, S = Nn(e.props), D = S ? n : k, F = S ? w : v;
      if (r === "svg" || Ha(k) ? r = "svg" : (r === "mathml" || Wa(k)) && (r = "mathml"), P ? (h(
        e.dynamicChildren,
        P,
        D,
        i,
        o,
        r,
        a
      ), ks(e, t, !0)) : l || u(
        e,
        t,
        D,
        F,
        i,
        o,
        r,
        a,
        !1
      ), y)
        S ? t.props && e.props && t.props.to !== e.props.to && (t.props.to = e.props.to) : ni(
          t,
          n,
          w,
          c,
          1
        );
      else if ((t.props && t.props.to) !== (e.props && e.props.to)) {
        const z = t.target = pr(
          t.props,
          p
        );
        z ? ni(
          t,
          z,
          null,
          c,
          0
        ) : x.NODE_ENV !== "production" && R(
          "Invalid Teleport target on update:",
          k,
          `(${typeof k})`
        );
      } else S && ni(
        t,
        k,
        v,
        c,
        1
      );
      Mi(t, y);
    }
  },
  remove(e, t, n, { um: s, o: { remove: i } }, o) {
    const {
      shapeFlag: r,
      children: a,
      anchor: l,
      targetStart: c,
      targetAnchor: f,
      target: u,
      props: h
    } = e;
    if (u && (i(c), i(f)), o && i(l), r & 16) {
      const d = o || !Nn(h);
      for (let p = 0; p < a.length; p++) {
        const g = a[p];
        s(
          g,
          t,
          n,
          d,
          !!g.dynamicChildren
        );
      }
    }
  },
  move: ni,
  hydrate: np
};
function ni(e, t, n, { o: { insert: s }, m: i }, o = 2) {
  o === 0 && s(e.targetAnchor, t, n);
  const { el: r, anchor: a, shapeFlag: l, children: c, props: f } = e, u = o === 2;
  if (u && s(r, t, n), (!u || Nn(f)) && l & 16)
    for (let h = 0; h < c.length; h++)
      i(
        c[h],
        t,
        n,
        2
      );
  u && s(a, t, n);
}
function np(e, t, n, s, i, o, {
  o: { nextSibling: r, parentNode: a, querySelector: l, insert: c, createText: f }
}, u) {
  const h = t.target = pr(
    t.props,
    l
  );
  if (h) {
    const d = Nn(t.props), p = h._lpa || h.firstChild;
    if (t.shapeFlag & 16)
      if (d)
        t.anchor = u(
          r(e),
          t,
          a(e),
          n,
          s,
          i,
          o
        ), t.targetStart = p, t.targetAnchor = p && r(p);
      else {
        t.anchor = r(e);
        let g = p;
        for (; g; ) {
          if (g && g.nodeType === 8) {
            if (g.data === "teleport start anchor")
              t.targetStart = g;
            else if (g.data === "teleport anchor") {
              t.targetAnchor = g, h._lpa = t.targetAnchor && r(t.targetAnchor);
              break;
            }
          }
          g = r(g);
        }
        t.targetAnchor || zf(h, t, f, c), u(
          p && r(p),
          t,
          h,
          n,
          s,
          i,
          o
        );
      }
    Mi(t, d);
  }
  return t.anchor && r(t.anchor);
}
const sp = jf;
function Mi(e, t) {
  const n = e.ctx;
  if (n && n.ut) {
    let s, i;
    for (t ? (s = e.el, i = e.anchor) : (s = e.targetStart, i = e.targetAnchor); s && s !== i; )
      s.nodeType === 1 && s.setAttribute("data-v-owner", n.uid), s = s.nextSibling;
    n.ut();
  }
}
function zf(e, t, n, s) {
  const i = t.targetStart = n(""), o = t.targetAnchor = n("");
  return i[Bf] = o, e && (s(i, e), s(o, e)), o;
}
function ta(e, t) {
  e.shapeFlag & 6 && e.component ? (e.transition = t, ta(e.component.subTree, t)) : e.shapeFlag & 128 ? (e.ssContent.transition = t.clone(e.ssContent), e.ssFallback.transition = t.clone(e.ssFallback)) : e.transition = t;
}
/*! #__NO_SIDE_EFFECTS__ */
// @__NO_SIDE_EFFECTS__
function ip(e, t) {
  return K(e) ? (
    // #8236: extend call and options.name access are considered side-effects
    // by Rollup, so we have to wrap it in a pure-annotated IIFE.
    _t({ name: e.name }, t, { setup: e })
  ) : e;
}
function Hf(e) {
  e.ids = [e.ids[0] + e.ids[2]++ + "-", 0, 0];
}
const op = /* @__PURE__ */ new WeakSet();
function Hi(e, t, n, s, i = !1) {
  if (U(e)) {
    e.forEach(
      (p, g) => Hi(
        p,
        t && (U(t) ? t[g] : t),
        n,
        s,
        i
      )
    );
    return;
  }
  if (Ms(s) && !i) {
    s.shapeFlag & 512 && s.type.__asyncResolved && s.component.subTree.component && Hi(e, t, n, s.component.subTree);
    return;
  }
  const o = s.shapeFlag & 4 ? ra(s.component) : s.el, r = i ? null : o, { i: a, r: l } = e;
  if (x.NODE_ENV !== "production" && !a) {
    R(
      "Missing ref owner context. ref cannot be used on hoisted vnodes. A vnode with ref must be created inside the render function."
    );
    return;
  }
  const c = t && t.r, f = a.refs === ut ? a.refs = {} : a.refs, u = a.setupState, h = et(u), d = u === ut ? () => !1 : (p) => x.NODE_ENV !== "production" && (at(h, p) && !kt(h[p]) && R(
    `Template ref "${p}" used on a non-ref value. It will not work in the production build.`
  ), op.has(h[p])) ? !1 : at(h, p);
  if (c != null && c !== l && (bt(c) ? (f[c] = null, d(c) && (u[c] = null)) : kt(c) && (c.value = null)), K(l))
    Jn(l, a, 12, [r, f]);
  else {
    const p = bt(l), g = kt(l);
    if (p || g) {
      const b = () => {
        if (e.f) {
          const y = p ? d(l) ? u[l] : f[l] : l.value;
          i ? U(y) && zr(y, o) : U(y) ? y.includes(o) || y.push(o) : p ? (f[l] = [o], d(l) && (u[l] = f[l])) : (l.value = [o], e.k && (f[e.k] = l.value));
        } else p ? (f[l] = r, d(l) && (u[l] = r)) : g ? (l.value = r, e.k && (f[e.k] = r)) : x.NODE_ENV !== "production" && R("Invalid template ref type:", l, `(${typeof l})`);
      };
      r ? (b.id = -1, Bt(b, n)) : b();
    } else x.NODE_ENV !== "production" && R("Invalid template ref type:", l, `(${typeof l})`);
  }
}
Ys().requestIdleCallback;
Ys().cancelIdleCallback;
const Ms = (e) => !!e.type.__asyncLoader, ea = (e) => e.type.__isKeepAlive;
function rp(e, t) {
  Wf(e, "a", t);
}
function ap(e, t) {
  Wf(e, "da", t);
}
function Wf(e, t, n = Dt) {
  const s = e.__wdc || (e.__wdc = () => {
    let i = n;
    for (; i; ) {
      if (i.isDeactivated)
        return;
      i = i.parent;
    }
    return e();
  });
  if (go(t, s, n), n) {
    let i = n.parent;
    for (; i && i.parent; )
      ea(i.parent.vnode) && lp(s, t, n, i), i = i.parent;
  }
}
function lp(e, t, n, s) {
  const i = go(
    t,
    e,
    s,
    !0
    /* prepend */
  );
  Uf(() => {
    zr(s[t], i);
  }, n);
}
function go(e, t, n = Dt, s = !1) {
  if (n) {
    const i = n[e] || (n[e] = []), o = t.__weh || (t.__weh = (...r) => {
      Ke();
      const a = Gs(n), l = Ve(t, n, e, r);
      return a(), qe(), l;
    });
    return s ? i.unshift(o) : i.push(o), o;
  } else if (x.NODE_ENV !== "production") {
    const i = bn(Zr[e].replace(/ hook$/, ""));
    R(
      `${i} is called when there is no active component instance to be associated with. Lifecycle injection APIs can only be used during execution of setup(). If you are using async setup(), make sure to register lifecycle hooks before the first await statement.`
    );
  }
}
const Xe = (e) => (t, n = Dt) => {
  (!$s || e === "sp") && go(e, (...s) => t(...s), n);
}, cp = Xe("bm"), fp = Xe("m"), up = Xe(
  "bu"
), hp = Xe("u"), dp = Xe(
  "bum"
), Uf = Xe("um"), pp = Xe(
  "sp"
), gp = Xe("rtg"), mp = Xe("rtc");
function bp(e, t = Dt) {
  go("ec", e, t);
}
const _p = Symbol.for("v-ndc");
function yp(e, t, n, s) {
  let i;
  const o = n, r = U(e);
  if (r || bt(e)) {
    const a = r && Mn(e);
    let l = !1;
    a && (l = !qt(e), e = fo(e)), i = new Array(e.length);
    for (let c = 0, f = e.length; c < f; c++)
      i[c] = t(
        l ? Ut(e[c]) : e[c],
        c,
        void 0,
        o
      );
  } else if (typeof e == "number") {
    x.NODE_ENV !== "production" && !Number.isInteger(e) && R(`The v-for range expect an integer value but got ${e}.`), i = new Array(e);
    for (let a = 0; a < e; a++)
      i[a] = t(a + 1, a, void 0, o);
  } else if (dt(e))
    if (e[Symbol.iterator])
      i = Array.from(
        e,
        (a, l) => t(a, l, void 0, o)
      );
    else {
      const a = Object.keys(e);
      i = new Array(a.length);
      for (let l = 0, c = a.length; l < c; l++) {
        const f = a[l];
        i[l] = t(e[f], f, l, o);
      }
    }
  else
    i = [];
  return i;
}
const gr = (e) => e ? mu(e) ? ra(e) : gr(e.parent) : null, Dn = (
  // Move PURE marker to new line to workaround compiler discarding it
  // due to type annotation
  /* @__PURE__ */ _t(/* @__PURE__ */ Object.create(null), {
    $: (e) => e,
    $el: (e) => e.vnode.el,
    $data: (e) => e.data,
    $props: (e) => x.NODE_ENV !== "production" ? ke(e.props) : e.props,
    $attrs: (e) => x.NODE_ENV !== "production" ? ke(e.attrs) : e.attrs,
    $slots: (e) => x.NODE_ENV !== "production" ? ke(e.slots) : e.slots,
    $refs: (e) => x.NODE_ENV !== "production" ? ke(e.refs) : e.refs,
    $parent: (e) => gr(e.parent),
    $root: (e) => gr(e.root),
    $host: (e) => e.ce,
    $emit: (e) => e.emit,
    $options: (e) => qf(e),
    $forceUpdate: (e) => e.f || (e.f = () => {
      po(e.update);
    }),
    $nextTick: (e) => e.n || (e.n = Df.bind(e.proxy)),
    $watch: (e) => Jp.bind(e)
  })
), na = (e) => e === "_" || e === "$", Po = (e, t) => e !== ut && !e.__isScriptSetup && at(e, t), Yf = {
  get({ _: e }, t) {
    if (t === "__v_skip")
      return !0;
    const { ctx: n, setupState: s, data: i, props: o, accessCache: r, type: a, appContext: l } = e;
    if (x.NODE_ENV !== "production" && t === "__isVue")
      return !0;
    let c;
    if (t[0] !== "$") {
      const d = r[t];
      if (d !== void 0)
        switch (d) {
          case 1:
            return s[t];
          case 2:
            return i[t];
          case 4:
            return n[t];
          case 3:
            return o[t];
        }
      else {
        if (Po(s, t))
          return r[t] = 1, s[t];
        if (i !== ut && at(i, t))
          return r[t] = 2, i[t];
        if (
          // only cache other properties when instance has declared (thus stable)
          // props
          (c = e.propsOptions[0]) && at(c, t)
        )
          return r[t] = 3, o[t];
        if (n !== ut && at(n, t))
          return r[t] = 4, n[t];
        mr && (r[t] = 0);
      }
    }
    const f = Dn[t];
    let u, h;
    if (f)
      return t === "$attrs" ? (Ot(e.attrs, "get", ""), x.NODE_ENV !== "production" && Yi()) : x.NODE_ENV !== "production" && t === "$slots" && Ot(e, "get", t), f(e);
    if (
      // css module (injected by vue-loader)
      (u = a.__cssModules) && (u = u[t])
    )
      return u;
    if (n !== ut && at(n, t))
      return r[t] = 4, n[t];
    if (
      // global properties
      h = l.config.globalProperties, at(h, t)
    )
      return h[t];
    x.NODE_ENV !== "production" && Jt && (!bt(t) || // #1091 avoid internal isRef/isVNode checks on component instance leading
    // to infinite warning loop
    t.indexOf("__v") !== 0) && (i !== ut && na(t[0]) && at(i, t) ? R(
      `Property ${JSON.stringify(
        t
      )} must be accessed via $data because it starts with a reserved character ("$" or "_") and is not proxied on the render context.`
    ) : e === Jt && R(
      `Property ${JSON.stringify(t)} was accessed during render but is not defined on instance.`
    ));
  },
  set({ _: e }, t, n) {
    const { data: s, setupState: i, ctx: o } = e;
    return Po(i, t) ? (i[t] = n, !0) : x.NODE_ENV !== "production" && i.__isScriptSetup && at(i, t) ? (R(`Cannot mutate <script setup> binding "${t}" from Options API.`), !1) : s !== ut && at(s, t) ? (s[t] = n, !0) : at(e.props, t) ? (x.NODE_ENV !== "production" && R(`Attempting to mutate prop "${t}". Props are readonly.`), !1) : t[0] === "$" && t.slice(1) in e ? (x.NODE_ENV !== "production" && R(
      `Attempting to mutate public property "${t}". Properties starting with $ are reserved and readonly.`
    ), !1) : (x.NODE_ENV !== "production" && t in e.appContext.config.globalProperties ? Object.defineProperty(o, t, {
      enumerable: !0,
      configurable: !0,
      value: n
    }) : o[t] = n, !0);
  },
  has({
    _: { data: e, setupState: t, accessCache: n, ctx: s, appContext: i, propsOptions: o }
  }, r) {
    let a;
    return !!n[r] || e !== ut && at(e, r) || Po(t, r) || (a = o[0]) && at(a, r) || at(s, r) || at(Dn, r) || at(i.config.globalProperties, r);
  },
  defineProperty(e, t, n) {
    return n.get != null ? e._.accessCache[t] = 0 : at(n, "value") && this.set(e, t, n.value, null), Reflect.defineProperty(e, t, n);
  }
};
x.NODE_ENV !== "production" && (Yf.ownKeys = (e) => (R(
  "Avoid app logic that relies on enumerating keys on a component instance. The keys will be empty in production mode to avoid performance overhead."
), Reflect.ownKeys(e)));
function xp(e) {
  const t = {};
  return Object.defineProperty(t, "_", {
    configurable: !0,
    enumerable: !1,
    get: () => e
  }), Object.keys(Dn).forEach((n) => {
    Object.defineProperty(t, n, {
      configurable: !0,
      enumerable: !1,
      get: () => Dn[n](e),
      // intercepted by the proxy so no need for implementation,
      // but needed to prevent set errors
      set: St
    });
  }), t;
}
function vp(e) {
  const {
    ctx: t,
    propsOptions: [n]
  } = e;
  n && Object.keys(n).forEach((s) => {
    Object.defineProperty(t, s, {
      enumerable: !0,
      configurable: !0,
      get: () => e.props[s],
      set: St
    });
  });
}
function wp(e) {
  const { ctx: t, setupState: n } = e;
  Object.keys(et(n)).forEach((s) => {
    if (!n.__isScriptSetup) {
      if (na(s[0])) {
        R(
          `setup() return property ${JSON.stringify(
            s
          )} should not start with "$" or "_" which are reserved prefixes for Vue internals.`
        );
        return;
      }
      Object.defineProperty(t, s, {
        enumerable: !0,
        configurable: !0,
        get: () => n[s],
        set: St
      });
    }
  });
}
function Ua(e) {
  return U(e) ? e.reduce(
    (t, n) => (t[n] = null, t),
    {}
  ) : e;
}
function Ep() {
  const e = /* @__PURE__ */ Object.create(null);
  return (t, n) => {
    e[n] ? R(`${t} property "${n}" is already defined in ${e[n]}.`) : e[n] = t;
  };
}
let mr = !0;
function Op(e) {
  const t = qf(e), n = e.proxy, s = e.ctx;
  mr = !1, t.beforeCreate && Ya(t.beforeCreate, e, "bc");
  const {
    // state
    data: i,
    computed: o,
    methods: r,
    watch: a,
    provide: l,
    inject: c,
    // lifecycle
    created: f,
    beforeMount: u,
    mounted: h,
    beforeUpdate: d,
    updated: p,
    activated: g,
    deactivated: b,
    beforeDestroy: y,
    beforeUnmount: O,
    destroyed: M,
    unmounted: P,
    render: w,
    renderTracked: k,
    renderTriggered: v,
    errorCaptured: S,
    serverPrefetch: D,
    // public API
    expose: F,
    inheritAttrs: z,
    // assets
    components: j,
    directives: tt,
    filters: Et
  } = t, it = x.NODE_ENV !== "production" ? Ep() : null;
  if (x.NODE_ENV !== "production") {
    const [W] = e.propsOptions;
    if (W)
      for (const G in W)
        it("Props", G);
  }
  if (c && Sp(c, s, it), r)
    for (const W in r) {
      const G = r[W];
      K(G) ? (x.NODE_ENV !== "production" ? Object.defineProperty(s, W, {
        value: G.bind(n),
        configurable: !0,
        enumerable: !0,
        writable: !0
      }) : s[W] = G.bind(n), x.NODE_ENV !== "production" && it("Methods", W)) : x.NODE_ENV !== "production" && R(
        `Method "${W}" has type "${typeof G}" in the component definition. Did you reference the function correctly?`
      );
    }
  if (i) {
    x.NODE_ENV !== "production" && !K(i) && R(
      "The data option must be a function. Plain object usage is no longer supported."
    );
    const W = i.call(n, n);
    if (x.NODE_ENV !== "production" && Hr(W) && R(
      "data() returned a Promise - note data() cannot be async; If you intend to perform data fetching before component renders, use async setup() + <Suspense>."
    ), !dt(W))
      x.NODE_ENV !== "production" && R("data() should return an object.");
    else if (e.data = Gr(W), x.NODE_ENV !== "production")
      for (const G in W)
        it("Data", G), na(G[0]) || Object.defineProperty(s, G, {
          configurable: !0,
          enumerable: !0,
          get: () => W[G],
          set: St
        });
  }
  if (mr = !0, o)
    for (const W in o) {
      const G = o[W], Ct = K(G) ? G.bind(n, n) : K(G.get) ? G.get.bind(n, n) : St;
      x.NODE_ENV !== "production" && Ct === St && R(`Computed property "${W}" has no getter.`);
      const re = !K(G) && K(G.set) ? G.set.bind(n) : x.NODE_ENV !== "production" ? () => {
        R(
          `Write operation failed: computed property "${W}" is readonly.`
        );
      } : St, ee = Og({
        get: Ct,
        set: re
      });
      Object.defineProperty(s, W, {
        enumerable: !0,
        configurable: !0,
        get: () => ee.value,
        set: (It) => ee.value = It
      }), x.NODE_ENV !== "production" && it("Computed", W);
    }
  if (a)
    for (const W in a)
      Kf(a[W], s, n, W);
  if (l) {
    const W = K(l) ? l.call(n) : l;
    Reflect.ownKeys(W).forEach((G) => {
      Pp(G, W[G]);
    });
  }
  f && Ya(f, e, "c");
  function st(W, G) {
    U(G) ? G.forEach((Ct) => W(Ct.bind(n))) : G && W(G.bind(n));
  }
  if (st(cp, u), st(fp, h), st(up, d), st(hp, p), st(rp, g), st(ap, b), st(bp, S), st(mp, k), st(gp, v), st(dp, O), st(Uf, P), st(pp, D), U(F))
    if (F.length) {
      const W = e.exposed || (e.exposed = {});
      F.forEach((G) => {
        Object.defineProperty(W, G, {
          get: () => n[G],
          set: (Ct) => n[G] = Ct
        });
      });
    } else e.exposed || (e.exposed = {});
  w && e.render === St && (e.render = w), z != null && (e.inheritAttrs = z), j && (e.components = j), tt && (e.directives = tt), D && Hf(e);
}
function Sp(e, t, n = St) {
  U(e) && (e = br(e));
  for (const s in e) {
    const i = e[s];
    let o;
    dt(i) ? "default" in i ? o = ki(
      i.from || s,
      i.default,
      !0
    ) : o = ki(i.from || s) : o = ki(i), kt(o) ? Object.defineProperty(t, s, {
      enumerable: !0,
      configurable: !0,
      get: () => o.value,
      set: (r) => o.value = r
    }) : t[s] = o, x.NODE_ENV !== "production" && n("Inject", s);
  }
}
function Ya(e, t, n) {
  Ve(
    U(e) ? e.map((s) => s.bind(t.proxy)) : e.bind(t.proxy),
    t,
    n
  );
}
function Kf(e, t, n, s) {
  let i = s.includes(".") ? au(n, s) : () => n[s];
  if (bt(e)) {
    const o = t[e];
    K(o) ? Ao(i, o) : x.NODE_ENV !== "production" && R(`Invalid watch handler specified by key "${e}"`, o);
  } else if (K(e))
    Ao(i, e.bind(n));
  else if (dt(e))
    if (U(e))
      e.forEach((o) => Kf(o, t, n, s));
    else {
      const o = K(e.handler) ? e.handler.bind(n) : t[e.handler];
      K(o) ? Ao(i, o, e) : x.NODE_ENV !== "production" && R(`Invalid watch handler specified by key "${e.handler}"`, o);
    }
  else x.NODE_ENV !== "production" && R(`Invalid watch option: "${s}"`, e);
}
function qf(e) {
  const t = e.type, { mixins: n, extends: s } = t, {
    mixins: i,
    optionsCache: o,
    config: { optionMergeStrategies: r }
  } = e.appContext, a = o.get(t);
  let l;
  return a ? l = a : !i.length && !n && !s ? l = t : (l = {}, i.length && i.forEach(
    (c) => Wi(l, c, r, !0)
  ), Wi(l, t, r)), dt(t) && o.set(t, l), l;
}
function Wi(e, t, n, s = !1) {
  const { mixins: i, extends: o } = t;
  o && Wi(e, o, n, !0), i && i.forEach(
    (r) => Wi(e, r, n, !0)
  );
  for (const r in t)
    if (s && r === "expose")
      x.NODE_ENV !== "production" && R(
        '"expose" option is ignored when declared in mixins or extends. It should only be declared in the base component itself.'
      );
    else {
      const a = Mp[r] || n && n[r];
      e[r] = a ? a(e[r], t[r]) : t[r];
    }
  return e;
}
const Mp = {
  data: Ka,
  props: qa,
  emits: qa,
  // objects
  methods: _s,
  computed: _s,
  // lifecycle
  beforeCreate: $t,
  created: $t,
  beforeMount: $t,
  mounted: $t,
  beforeUpdate: $t,
  updated: $t,
  beforeDestroy: $t,
  beforeUnmount: $t,
  destroyed: $t,
  unmounted: $t,
  activated: $t,
  deactivated: $t,
  errorCaptured: $t,
  serverPrefetch: $t,
  // assets
  components: _s,
  directives: _s,
  // watch
  watch: Np,
  // provide / inject
  provide: Ka,
  inject: kp
};
function Ka(e, t) {
  return t ? e ? function() {
    return _t(
      K(e) ? e.call(this, this) : e,
      K(t) ? t.call(this, this) : t
    );
  } : t : e;
}
function kp(e, t) {
  return _s(br(e), br(t));
}
function br(e) {
  if (U(e)) {
    const t = {};
    for (let n = 0; n < e.length; n++)
      t[e[n]] = e[n];
    return t;
  }
  return e;
}
function $t(e, t) {
  return e ? [...new Set([].concat(e, t))] : t;
}
function _s(e, t) {
  return e ? _t(/* @__PURE__ */ Object.create(null), e, t) : t;
}
function qa(e, t) {
  return e ? U(e) && U(t) ? [.../* @__PURE__ */ new Set([...e, ...t])] : _t(
    /* @__PURE__ */ Object.create(null),
    Ua(e),
    Ua(t ?? {})
  ) : t;
}
function Np(e, t) {
  if (!e) return t;
  if (!t) return e;
  const n = _t(/* @__PURE__ */ Object.create(null), e);
  for (const s in t)
    n[s] = $t(e[s], t[s]);
  return n;
}
function Xf() {
  return {
    app: null,
    config: {
      isNativeTag: Wh,
      performance: !1,
      globalProperties: {},
      optionMergeStrategies: {},
      errorHandler: void 0,
      warnHandler: void 0,
      compilerOptions: {}
    },
    mixins: [],
    components: {},
    directives: {},
    provides: /* @__PURE__ */ Object.create(null),
    optionsCache: /* @__PURE__ */ new WeakMap(),
    propsCache: /* @__PURE__ */ new WeakMap(),
    emitsCache: /* @__PURE__ */ new WeakMap()
  };
}
let Dp = 0;
function Cp(e, t) {
  return function(s, i = null) {
    K(s) || (s = _t({}, s)), i != null && !dt(i) && (x.NODE_ENV !== "production" && R("root props passed to app.mount() must be an object."), i = null);
    const o = Xf(), r = /* @__PURE__ */ new WeakSet(), a = [];
    let l = !1;
    const c = o.app = {
      _uid: Dp++,
      _component: s,
      _props: i,
      _container: null,
      _context: o,
      _instance: null,
      version: rl,
      get config() {
        return o.config;
      },
      set config(f) {
        x.NODE_ENV !== "production" && R(
          "app.config cannot be replaced. Modify individual options instead."
        );
      },
      use(f, ...u) {
        return r.has(f) ? x.NODE_ENV !== "production" && R("Plugin has already been applied to target app.") : f && K(f.install) ? (r.add(f), f.install(c, ...u)) : K(f) ? (r.add(f), f(c, ...u)) : x.NODE_ENV !== "production" && R(
          'A plugin must either be a function or an object with an "install" function.'
        ), c;
      },
      mixin(f) {
        return o.mixins.includes(f) ? x.NODE_ENV !== "production" && R(
          "Mixin has already been applied to target app" + (f.name ? `: ${f.name}` : "")
        ) : o.mixins.push(f), c;
      },
      component(f, u) {
        return x.NODE_ENV !== "production" && wr(f, o.config), u ? (x.NODE_ENV !== "production" && o.components[f] && R(`Component "${f}" has already been registered in target app.`), o.components[f] = u, c) : o.components[f];
      },
      directive(f, u) {
        return x.NODE_ENV !== "production" && $f(f), u ? (x.NODE_ENV !== "production" && o.directives[f] && R(`Directive "${f}" has already been registered in target app.`), o.directives[f] = u, c) : o.directives[f];
      },
      mount(f, u, h) {
        if (l)
          x.NODE_ENV !== "production" && R(
            "App has already been mounted.\nIf you want to remount the same app, move your app creation logic into a factory function and create fresh app instances for each mount - e.g. `const createMyApp = () => createApp(App)`"
          );
        else {
          x.NODE_ENV !== "production" && f.__vue_app__ && R(
            "There is already an app instance mounted on the host container.\n If you want to mount another app on the same host container, you need to unmount the previous app by calling `app.unmount()` first."
          );
          const d = c._ceVNode || De(s, i);
          return d.appContext = o, h === !0 ? h = "svg" : h === !1 && (h = void 0), x.NODE_ENV !== "production" && (o.reload = () => {
            e(
              on(d),
              f,
              h
            );
          }), e(d, f, h), l = !0, c._container = f, f.__vue_app__ = c, x.NODE_ENV !== "production" && (c._instance = d.component, Yd(c, rl)), ra(d.component);
        }
      },
      onUnmount(f) {
        x.NODE_ENV !== "production" && typeof f != "function" && R(
          `Expected function as first argument to app.onUnmount(), but got ${typeof f}`
        ), a.push(f);
      },
      unmount() {
        l ? (Ve(
          a,
          c._instance,
          16
        ), e(null, c._container), x.NODE_ENV !== "production" && (c._instance = null, Kd(c)), delete c._container.__vue_app__) : x.NODE_ENV !== "production" && R("Cannot unmount an app that is not mounted.");
      },
      provide(f, u) {
        return x.NODE_ENV !== "production" && f in o.provides && R(
          `App already provides property with key "${String(f)}". It will be overwritten with the new value.`
        ), o.provides[f] = u, c;
      },
      runWithContext(f) {
        const u = Yn;
        Yn = c;
        try {
          return f();
        } finally {
          Yn = u;
        }
      }
    };
    return c;
  };
}
let Yn = null;
function Pp(e, t) {
  if (!Dt)
    x.NODE_ENV !== "production" && R("provide() can only be used inside setup().");
  else {
    let n = Dt.provides;
    const s = Dt.parent && Dt.parent.provides;
    s === n && (n = Dt.provides = Object.create(s)), n[e] = t;
  }
}
function ki(e, t, n = !1) {
  const s = Dt || Jt;
  if (s || Yn) {
    const i = Yn ? Yn._context.provides : s ? s.parent == null ? s.vnode.appContext && s.vnode.appContext.provides : s.parent.provides : void 0;
    if (i && e in i)
      return i[e];
    if (arguments.length > 1)
      return n && K(t) ? t.call(s && s.proxy) : t;
    x.NODE_ENV !== "production" && R(`injection "${String(e)}" not found.`);
  } else x.NODE_ENV !== "production" && R("inject() can only be used inside setup() or functional components.");
}
const Gf = {}, Zf = () => Object.create(Gf), Jf = (e) => Object.getPrototypeOf(e) === Gf;
function Tp(e, t, n, s = !1) {
  const i = {}, o = Zf();
  e.propsDefaults = /* @__PURE__ */ Object.create(null), Qf(e, t, i, o);
  for (const r in e.propsOptions[0])
    r in i || (i[r] = void 0);
  x.NODE_ENV !== "production" && eu(t || {}, i, e), n ? e.props = s ? i : Nd(i) : e.type.props ? e.props = i : e.props = o, e.attrs = o;
}
function Ap(e) {
  for (; e; ) {
    if (e.type.__hmrId) return !0;
    e = e.parent;
  }
}
function Vp(e, t, n, s) {
  const {
    props: i,
    attrs: o,
    vnode: { patchFlag: r }
  } = e, a = et(i), [l] = e.propsOptions;
  let c = !1;
  if (
    // always force full diff in dev
    // - #1942 if hmr is enabled with sfc component
    // - vite#872 non-sfc component used by sfc component
    !(x.NODE_ENV !== "production" && Ap(e)) && (s || r > 0) && !(r & 16)
  ) {
    if (r & 8) {
      const f = e.vnode.dynamicProps;
      for (let u = 0; u < f.length; u++) {
        let h = f[u];
        if (mo(e.emitsOptions, h))
          continue;
        const d = t[h];
        if (l)
          if (at(o, h))
            d !== o[h] && (o[h] = d, c = !0);
          else {
            const p = Kt(h);
            i[p] = _r(
              l,
              a,
              p,
              d,
              e,
              !1
            );
          }
        else
          d !== o[h] && (o[h] = d, c = !0);
      }
    }
  } else {
    Qf(e, t, i, o) && (c = !0);
    let f;
    for (const u in a)
      (!t || // for camelCase
      !at(t, u) && // it's possible the original props was passed in as kebab-case
      // and converted to camelCase (#955)
      ((f = Zt(u)) === u || !at(t, f))) && (l ? n && // for camelCase
      (n[u] !== void 0 || // for kebab-case
      n[f] !== void 0) && (i[u] = _r(
        l,
        a,
        u,
        void 0,
        e,
        !0
      )) : delete i[u]);
    if (o !== a)
      for (const u in o)
        (!t || !at(t, u)) && (delete o[u], c = !0);
  }
  c && Se(e.attrs, "set", ""), x.NODE_ENV !== "production" && eu(t || {}, i, e);
}
function Qf(e, t, n, s) {
  const [i, o] = e.propsOptions;
  let r = !1, a;
  if (t)
    for (let l in t) {
      if (Es(l))
        continue;
      const c = t[l];
      let f;
      i && at(i, f = Kt(l)) ? !o || !o.includes(f) ? n[f] = c : (a || (a = {}))[f] = c : mo(e.emitsOptions, l) || (!(l in s) || c !== s[l]) && (s[l] = c, r = !0);
    }
  if (o) {
    const l = et(n), c = a || ut;
    for (let f = 0; f < o.length; f++) {
      const u = o[f];
      n[u] = _r(
        i,
        l,
        u,
        c[u],
        e,
        !at(c, u)
      );
    }
  }
  return r;
}
function _r(e, t, n, s, i, o) {
  const r = e[n];
  if (r != null) {
    const a = at(r, "default");
    if (a && s === void 0) {
      const l = r.default;
      if (r.type !== Function && !r.skipFactory && K(l)) {
        const { propsDefaults: c } = i;
        if (n in c)
          s = c[n];
        else {
          const f = Gs(i);
          s = c[n] = l.call(
            null,
            t
          ), f();
        }
      } else
        s = l;
      i.ce && i.ce._setProp(n, s);
    }
    r[
      0
      /* shouldCast */
    ] && (o && !a ? s = !1 : r[
      1
      /* shouldCastTrue */
    ] && (s === "" || s === Zt(n)) && (s = !0));
  }
  return s;
}
const Rp = /* @__PURE__ */ new WeakMap();
function tu(e, t, n = !1) {
  const s = n ? Rp : t.propsCache, i = s.get(e);
  if (i)
    return i;
  const o = e.props, r = {}, a = [];
  let l = !1;
  if (!K(e)) {
    const f = (u) => {
      l = !0;
      const [h, d] = tu(u, t, !0);
      _t(r, h), d && a.push(...d);
    };
    !n && t.mixins.length && t.mixins.forEach(f), e.extends && f(e.extends), e.mixins && e.mixins.forEach(f);
  }
  if (!o && !l)
    return dt(e) && s.set(e, Wn), Wn;
  if (U(o))
    for (let f = 0; f < o.length; f++) {
      x.NODE_ENV !== "production" && !bt(o[f]) && R("props must be strings when using array syntax.", o[f]);
      const u = Kt(o[f]);
      Xa(u) && (r[u] = ut);
    }
  else if (o) {
    x.NODE_ENV !== "production" && !dt(o) && R("invalid props options", o);
    for (const f in o) {
      const u = Kt(f);
      if (Xa(u)) {
        const h = o[f], d = r[u] = U(h) || K(h) ? { type: h } : _t({}, h), p = d.type;
        let g = !1, b = !0;
        if (U(p))
          for (let y = 0; y < p.length; ++y) {
            const O = p[y], M = K(O) && O.name;
            if (M === "Boolean") {
              g = !0;
              break;
            } else M === "String" && (b = !1);
          }
        else
          g = K(p) && p.name === "Boolean";
        d[
          0
          /* shouldCast */
        ] = g, d[
          1
          /* shouldCastTrue */
        ] = b, (g || at(d, "default")) && a.push(u);
      }
    }
  }
  const c = [r, a];
  return dt(e) && s.set(e, c), c;
}
function Xa(e) {
  return e[0] !== "$" && !Es(e) ? !0 : (x.NODE_ENV !== "production" && R(`Invalid prop name: "${e}" is a reserved property.`), !1);
}
function Ip(e) {
  return e === null ? "null" : typeof e == "function" ? e.name || "" : typeof e == "object" && e.constructor && e.constructor.name || "";
}
function eu(e, t, n) {
  const s = et(t), i = n.propsOptions[0], o = Object.keys(e).map((r) => Kt(r));
  for (const r in i) {
    let a = i[r];
    a != null && Lp(
      r,
      s[r],
      a,
      x.NODE_ENV !== "production" ? ke(s) : s,
      !o.includes(r)
    );
  }
}
function Lp(e, t, n, s, i) {
  const { type: o, required: r, validator: a, skipCheck: l } = n;
  if (r && i) {
    R('Missing required prop: "' + e + '"');
    return;
  }
  if (!(t == null && !r)) {
    if (o != null && o !== !0 && !l) {
      let c = !1;
      const f = U(o) ? o : [o], u = [];
      for (let h = 0; h < f.length && !c; h++) {
        const { valid: d, expectedType: p } = $p(t, f[h]);
        u.push(p || ""), c = d;
      }
      if (!c) {
        R(Bp(e, t, u));
        return;
      }
    }
    a && !a(t, s) && R('Invalid prop: custom validator check failed for prop "' + e + '".');
  }
}
const Fp = /* @__PURE__ */ Ye(
  "String,Number,Boolean,Function,Symbol,BigInt"
);
function $p(e, t) {
  let n;
  const s = Ip(t);
  if (s === "null")
    n = e === null;
  else if (Fp(s)) {
    const i = typeof e;
    n = i === s.toLowerCase(), !n && i === "object" && (n = e instanceof t);
  } else s === "Object" ? n = dt(e) : s === "Array" ? n = U(e) : n = e instanceof t;
  return {
    valid: n,
    expectedType: s
  };
}
function Bp(e, t, n) {
  if (n.length === 0)
    return `Prop type [] for prop "${e}" won't match anything. Did you mean to use type Array instead?`;
  let s = `Invalid prop: type check failed for prop "${e}". Expected ${n.map(lo).join(" | ")}`;
  const i = n[0], o = Wr(t), r = Ga(t, i), a = Ga(t, o);
  return n.length === 1 && Za(i) && !jp(i, o) && (s += ` with value ${r}`), s += `, got ${o} `, Za(o) && (s += `with value ${a}.`), s;
}
function Ga(e, t) {
  return t === "String" ? `"${e}"` : t === "Number" ? `${Number(e)}` : `${e}`;
}
function Za(e) {
  return ["string", "number", "boolean"].some((n) => e.toLowerCase() === n);
}
function jp(...e) {
  return e.some((t) => t.toLowerCase() === "boolean");
}
const nu = (e) => e[0] === "_" || e === "$stable", sa = (e) => U(e) ? e.map(ce) : [ce(e)], zp = (e, t, n) => {
  if (t._n)
    return t;
  const s = tp((...i) => (x.NODE_ENV !== "production" && Dt && (!n || n.root === Dt.root) && R(
    `Slot "${e}" invoked outside of the render function: this will not track dependencies used in the slot. Invoke the slot function inside the render function instead.`
  ), sa(t(...i))), n);
  return s._c = !1, s;
}, su = (e, t, n) => {
  const s = e._ctx;
  for (const i in e) {
    if (nu(i)) continue;
    const o = e[i];
    if (K(o))
      t[i] = zp(i, o, s);
    else if (o != null) {
      x.NODE_ENV !== "production" && R(
        `Non-function value encountered for slot "${i}". Prefer function slots for better performance.`
      );
      const r = sa(o);
      t[i] = () => r;
    }
  }
}, iu = (e, t) => {
  x.NODE_ENV !== "production" && !ea(e.vnode) && R(
    "Non-function value encountered for default slot. Prefer function slots for better performance."
  );
  const n = sa(t);
  e.slots.default = () => n;
}, yr = (e, t, n) => {
  for (const s in t)
    (n || s !== "_") && (e[s] = t[s]);
}, Hp = (e, t, n) => {
  const s = e.slots = Zf();
  if (e.vnode.shapeFlag & 32) {
    const i = t._;
    i ? (yr(s, t, n), n && Li(s, "_", i, !0)) : su(t, s);
  } else t && iu(e, t);
}, Wp = (e, t, n) => {
  const { vnode: s, slots: i } = e;
  let o = !0, r = ut;
  if (s.shapeFlag & 32) {
    const a = t._;
    a ? x.NODE_ENV !== "production" && fe ? (yr(i, t, n), Se(e, "set", "$slots")) : n && a === 1 ? o = !1 : yr(i, t, n) : (o = !t.$stable, su(t, i)), r = t;
  } else t && (iu(e, t), r = { default: 1 });
  if (o)
    for (const a in i)
      !nu(a) && r[a] == null && delete i[a];
};
let fs, Qe;
function Ln(e, t) {
  e.appContext.config.performance && Ui() && Qe.mark(`vue-${t}-${e.uid}`), x.NODE_ENV !== "production" && Zd(e, t, Ui() ? Qe.now() : Date.now());
}
function Fn(e, t) {
  if (e.appContext.config.performance && Ui()) {
    const n = `vue-${t}-${e.uid}`, s = n + ":end";
    Qe.mark(s), Qe.measure(
      `<${_o(e, e.type)}> ${t}`,
      n,
      s
    ), Qe.clearMarks(n), Qe.clearMarks(s);
  }
  x.NODE_ENV !== "production" && Jd(e, t, Ui() ? Qe.now() : Date.now());
}
function Ui() {
  return fs !== void 0 || (typeof window < "u" && window.performance ? (fs = !0, Qe = window.performance) : fs = !1), fs;
}
function Up() {
  const e = [];
  if (x.NODE_ENV !== "production" && e.length) {
    const t = e.length > 1;
    console.warn(
      `Feature flag${t ? "s" : ""} ${e.join(", ")} ${t ? "are" : "is"} not explicitly defined. You are running the esm-bundler build of Vue, which expects these compile-time feature flags to be globally injected via the bundler config in order to get better tree-shaking in the production bundle.

For more details, see https://link.vuejs.org/feature-flags.`
    );
  }
}
const Bt = og;
function Yp(e) {
  return Kp(e);
}
function Kp(e, t) {
  Up();
  const n = Ys();
  n.__VUE__ = !0, x.NODE_ENV !== "production" && Rf(n.__VUE_DEVTOOLS_GLOBAL_HOOK__, n);
  const {
    insert: s,
    remove: i,
    patchProp: o,
    createElement: r,
    createText: a,
    createComment: l,
    setText: c,
    setElementText: f,
    parentNode: u,
    nextSibling: h,
    setScopeId: d = St,
    insertStaticContent: p
  } = e, g = (m, _, E, T = null, N = null, C = null, $ = void 0, L = null, I = x.NODE_ENV !== "production" && fe ? !1 : !!_.dynamicChildren) => {
    if (m === _)
      return;
    m && !us(m, _) && (T = Js(m), Nt(m, N, C, !0), m = null), _.patchFlag === -2 && (I = !1, _.dynamicChildren = null);
    const { type: A, ref: Y, shapeFlag: B } = _;
    switch (A) {
      case Xs:
        b(m, _, E, T);
        break;
      case te:
        y(m, _, E, T);
        break;
      case Ni:
        m == null ? O(_, E, T, $) : x.NODE_ENV !== "production" && M(m, _, E, $);
        break;
      case le:
        tt(
          m,
          _,
          E,
          T,
          N,
          C,
          $,
          L,
          I
        );
        break;
      default:
        B & 1 ? k(
          m,
          _,
          E,
          T,
          N,
          C,
          $,
          L,
          I
        ) : B & 6 ? Et(
          m,
          _,
          E,
          T,
          N,
          C,
          $,
          L,
          I
        ) : B & 64 || B & 128 ? A.process(
          m,
          _,
          E,
          T,
          N,
          C,
          $,
          L,
          I,
          rs
        ) : x.NODE_ENV !== "production" && R("Invalid VNode type:", A, `(${typeof A})`);
    }
    Y != null && N && Hi(Y, m && m.ref, C, _ || m, !_);
  }, b = (m, _, E, T) => {
    if (m == null)
      s(
        _.el = a(_.children),
        E,
        T
      );
    else {
      const N = _.el = m.el;
      _.children !== m.children && c(N, _.children);
    }
  }, y = (m, _, E, T) => {
    m == null ? s(
      _.el = l(_.children || ""),
      E,
      T
    ) : _.el = m.el;
  }, O = (m, _, E, T) => {
    [m.el, m.anchor] = p(
      m.children,
      _,
      E,
      T,
      m.el,
      m.anchor
    );
  }, M = (m, _, E, T) => {
    if (_.children !== m.children) {
      const N = h(m.anchor);
      w(m), [_.el, _.anchor] = p(
        _.children,
        E,
        N,
        T
      );
    } else
      _.el = m.el, _.anchor = m.anchor;
  }, P = ({ el: m, anchor: _ }, E, T) => {
    let N;
    for (; m && m !== _; )
      N = h(m), s(m, E, T), m = N;
    s(_, E, T);
  }, w = ({ el: m, anchor: _ }) => {
    let E;
    for (; m && m !== _; )
      E = h(m), i(m), m = E;
    i(_);
  }, k = (m, _, E, T, N, C, $, L, I) => {
    _.type === "svg" ? $ = "svg" : _.type === "math" && ($ = "mathml"), m == null ? v(
      _,
      E,
      T,
      N,
      C,
      $,
      L,
      I
    ) : F(
      m,
      _,
      N,
      C,
      $,
      L,
      I
    );
  }, v = (m, _, E, T, N, C, $, L) => {
    let I, A;
    const { props: Y, shapeFlag: B, transition: H, dirs: X } = m;
    if (I = m.el = r(
      m.type,
      C,
      Y && Y.is,
      Y
    ), B & 8 ? f(I, m.children) : B & 16 && D(
      m.children,
      I,
      null,
      T,
      N,
      To(m, C),
      $,
      L
    ), X && hn(m, null, T, "created"), S(I, m, m.scopeId, $, T), Y) {
      for (const pt in Y)
        pt !== "value" && !Es(pt) && o(I, pt, null, Y[pt], C, T);
      "value" in Y && o(I, "value", null, Y.value, C), (A = Y.onVnodeBeforeMount) && ye(A, T, m);
    }
    x.NODE_ENV !== "production" && (Li(I, "__vnode", m, !0), Li(I, "__vueParentComponent", T, !0)), X && hn(m, null, T, "beforeMount");
    const rt = qp(N, H);
    rt && H.beforeEnter(I), s(I, _, E), ((A = Y && Y.onVnodeMounted) || rt || X) && Bt(() => {
      A && ye(A, T, m), rt && H.enter(I), X && hn(m, null, T, "mounted");
    }, N);
  }, S = (m, _, E, T, N) => {
    if (E && d(m, E), T)
      for (let C = 0; C < T.length; C++)
        d(m, T[C]);
    if (N) {
      let C = N.subTree;
      if (x.NODE_ENV !== "production" && C.patchFlag > 0 && C.patchFlag & 2048 && (C = ia(C.children) || C), _ === C || fu(C.type) && (C.ssContent === _ || C.ssFallback === _)) {
        const $ = N.vnode;
        S(
          m,
          $,
          $.scopeId,
          $.slotScopeIds,
          N.parent
        );
      }
    }
  }, D = (m, _, E, T, N, C, $, L, I = 0) => {
    for (let A = I; A < m.length; A++) {
      const Y = m[A] = L ? Ze(m[A]) : ce(m[A]);
      g(
        null,
        Y,
        _,
        E,
        T,
        N,
        C,
        $,
        L
      );
    }
  }, F = (m, _, E, T, N, C, $) => {
    const L = _.el = m.el;
    x.NODE_ENV !== "production" && (L.__vnode = _);
    let { patchFlag: I, dynamicChildren: A, dirs: Y } = _;
    I |= m.patchFlag & 16;
    const B = m.props || ut, H = _.props || ut;
    let X;
    if (E && dn(E, !1), (X = H.onVnodeBeforeUpdate) && ye(X, E, _, m), Y && hn(_, m, E, "beforeUpdate"), E && dn(E, !0), x.NODE_ENV !== "production" && fe && (I = 0, $ = !1, A = null), (B.innerHTML && H.innerHTML == null || B.textContent && H.textContent == null) && f(L, ""), A ? (z(
      m.dynamicChildren,
      A,
      L,
      E,
      T,
      To(_, N),
      C
    ), x.NODE_ENV !== "production" && ks(m, _)) : $ || Ct(
      m,
      _,
      L,
      null,
      E,
      T,
      To(_, N),
      C,
      !1
    ), I > 0) {
      if (I & 16)
        j(L, B, H, E, N);
      else if (I & 2 && B.class !== H.class && o(L, "class", null, H.class, N), I & 4 && o(L, "style", B.style, H.style, N), I & 8) {
        const rt = _.dynamicProps;
        for (let pt = 0; pt < rt.length; pt++) {
          const ct = rt[pt], Xt = B[ct], zt = H[ct];
          (zt !== Xt || ct === "value") && o(L, ct, Xt, zt, N, E);
        }
      }
      I & 1 && m.children !== _.children && f(L, _.children);
    } else !$ && A == null && j(L, B, H, E, N);
    ((X = H.onVnodeUpdated) || Y) && Bt(() => {
      X && ye(X, E, _, m), Y && hn(_, m, E, "updated");
    }, T);
  }, z = (m, _, E, T, N, C, $) => {
    for (let L = 0; L < _.length; L++) {
      const I = m[L], A = _[L], Y = (
        // oldVNode may be an errored async setup() component inside Suspense
        // which will not have a mounted element
        I.el && // - In the case of a Fragment, we need to provide the actual parent
        // of the Fragment itself so it can move its children.
        (I.type === le || // - In the case of different nodes, there is going to be a replacement
        // which also requires the correct parent container
        !us(I, A) || // - In the case of a component, it could contain anything.
        I.shapeFlag & 70) ? u(I.el) : (
          // In other cases, the parent container is not actually used so we
          // just pass the block element here to avoid a DOM parentNode call.
          E
        )
      );
      g(
        I,
        A,
        Y,
        null,
        T,
        N,
        C,
        $,
        !0
      );
    }
  }, j = (m, _, E, T, N) => {
    if (_ !== E) {
      if (_ !== ut)
        for (const C in _)
          !Es(C) && !(C in E) && o(
            m,
            C,
            _[C],
            null,
            N,
            T
          );
      for (const C in E) {
        if (Es(C)) continue;
        const $ = E[C], L = _[C];
        $ !== L && C !== "value" && o(m, C, L, $, N, T);
      }
      "value" in E && o(m, "value", _.value, E.value, N);
    }
  }, tt = (m, _, E, T, N, C, $, L, I) => {
    const A = _.el = m ? m.el : a(""), Y = _.anchor = m ? m.anchor : a("");
    let { patchFlag: B, dynamicChildren: H, slotScopeIds: X } = _;
    x.NODE_ENV !== "production" && // #5523 dev root fragment may inherit directives
    (fe || B & 2048) && (B = 0, I = !1, H = null), X && (L = L ? L.concat(X) : X), m == null ? (s(A, E, T), s(Y, E, T), D(
      // #10007
      // such fragment like `<></>` will be compiled into
      // a fragment which doesn't have a children.
      // In this case fallback to an empty array
      _.children || [],
      E,
      Y,
      N,
      C,
      $,
      L,
      I
    )) : B > 0 && B & 64 && H && // #2715 the previous fragment could've been a BAILed one as a result
    // of renderSlot() with no valid children
    m.dynamicChildren ? (z(
      m.dynamicChildren,
      H,
      E,
      N,
      C,
      $,
      L
    ), x.NODE_ENV !== "production" ? ks(m, _) : (
      // #2080 if the stable fragment has a key, it's a <template v-for> that may
      //  get moved around. Make sure all root level vnodes inherit el.
      // #2134 or if it's a component root, it may also get moved around
      // as the component is being moved.
      (_.key != null || N && _ === N.subTree) && ks(
        m,
        _,
        !0
        /* shallow */
      )
    )) : Ct(
      m,
      _,
      E,
      Y,
      N,
      C,
      $,
      L,
      I
    );
  }, Et = (m, _, E, T, N, C, $, L, I) => {
    _.slotScopeIds = L, m == null ? _.shapeFlag & 512 ? N.ctx.activate(
      _,
      E,
      T,
      $,
      I
    ) : it(
      _,
      E,
      T,
      N,
      C,
      $,
      I
    ) : st(m, _, I);
  }, it = (m, _, E, T, N, C, $) => {
    const L = m.component = pg(
      m,
      T,
      N
    );
    if (x.NODE_ENV !== "production" && L.type.__hmrId && zd(L), x.NODE_ENV !== "production" && (Ei(m), Ln(L, "mount")), ea(m) && (L.ctx.renderer = rs), x.NODE_ENV !== "production" && Ln(L, "init"), bg(L, !1, $), x.NODE_ENV !== "production" && Fn(L, "init"), L.asyncDep) {
      if (x.NODE_ENV !== "production" && fe && (m.el = null), N && N.registerDep(L, W, $), !m.el) {
        const I = L.subTree = De(te);
        y(null, I, _, E);
      }
    } else
      W(
        L,
        m,
        _,
        E,
        N,
        C,
        $
      );
    x.NODE_ENV !== "production" && (Oi(), Fn(L, "mount"));
  }, st = (m, _, E) => {
    const T = _.component = m.component;
    if (sg(m, _, E))
      if (T.asyncDep && !T.asyncResolved) {
        x.NODE_ENV !== "production" && Ei(_), G(T, _, E), x.NODE_ENV !== "production" && Oi();
        return;
      } else
        T.next = _, T.update();
    else
      _.el = m.el, T.vnode = _;
  }, W = (m, _, E, T, N, C, $) => {
    const L = () => {
      if (m.isMounted) {
        let { next: B, bu: H, u: X, parent: rt, vnode: pt } = m;
        {
          const be = ou(m);
          if (be) {
            B && (B.el = pt.el, G(m, B, $)), be.asyncDep.then(() => {
              m.isUnmounted || L();
            });
            return;
          }
        }
        let ct = B, Xt;
        x.NODE_ENV !== "production" && Ei(B || m.vnode), dn(m, !1), B ? (B.el = pt.el, G(m, B, $)) : B = pt, H && ls(H), (Xt = B.props && B.props.onVnodeBeforeUpdate) && ye(Xt, rt, B, pt), dn(m, !0), x.NODE_ENV !== "production" && Ln(m, "render");
        const zt = Qa(m);
        x.NODE_ENV !== "production" && Fn(m, "render");
        const me = m.subTree;
        m.subTree = zt, x.NODE_ENV !== "production" && Ln(m, "patch"), g(
          me,
          zt,
          // parent may have changed if it's in a teleport
          u(me.el),
          // anchor may have changed if it's in a fragment
          Js(me),
          m,
          N,
          C
        ), x.NODE_ENV !== "production" && Fn(m, "patch"), B.el = zt.el, ct === null && ig(m, zt.el), X && Bt(X, N), (Xt = B.props && B.props.onVnodeUpdated) && Bt(
          () => ye(Xt, rt, B, pt),
          N
        ), x.NODE_ENV !== "production" && If(m), x.NODE_ENV !== "production" && Oi();
      } else {
        let B;
        const { el: H, props: X } = _, { bm: rt, m: pt, parent: ct, root: Xt, type: zt } = m, me = Ms(_);
        dn(m, !1), rt && ls(rt), !me && (B = X && X.onVnodeBeforeMount) && ye(B, ct, _), dn(m, !0);
        {
          Xt.ce && Xt.ce._injectChildStyle(zt), x.NODE_ENV !== "production" && Ln(m, "render");
          const be = m.subTree = Qa(m);
          x.NODE_ENV !== "production" && Fn(m, "render"), x.NODE_ENV !== "production" && Ln(m, "patch"), g(
            null,
            be,
            E,
            T,
            m,
            N,
            C
          ), x.NODE_ENV !== "production" && Fn(m, "patch"), _.el = be.el;
        }
        if (pt && Bt(pt, N), !me && (B = X && X.onVnodeMounted)) {
          const be = _;
          Bt(
            () => ye(B, ct, be),
            N
          );
        }
        (_.shapeFlag & 256 || ct && Ms(ct.vnode) && ct.vnode.shapeFlag & 256) && m.a && Bt(m.a, N), m.isMounted = !0, x.NODE_ENV !== "production" && qd(m), _ = E = T = null;
      }
    };
    m.scope.on();
    const I = m.effect = new af(L);
    m.scope.off();
    const A = m.update = I.run.bind(I), Y = m.job = I.runIfDirty.bind(I);
    Y.i = m, Y.id = m.uid, I.scheduler = () => po(Y), dn(m, !0), x.NODE_ENV !== "production" && (I.onTrack = m.rtc ? (B) => ls(m.rtc, B) : void 0, I.onTrigger = m.rtg ? (B) => ls(m.rtg, B) : void 0), A();
  }, G = (m, _, E) => {
    _.component = m;
    const T = m.vnode.props;
    m.vnode = _, m.next = null, Vp(m, _.props, T, E), Wp(m, _.children, E), Ke(), Ba(m), qe();
  }, Ct = (m, _, E, T, N, C, $, L, I = !1) => {
    const A = m && m.children, Y = m ? m.shapeFlag : 0, B = _.children, { patchFlag: H, shapeFlag: X } = _;
    if (H > 0) {
      if (H & 128) {
        ee(
          A,
          B,
          E,
          T,
          N,
          C,
          $,
          L,
          I
        );
        return;
      } else if (H & 256) {
        re(
          A,
          B,
          E,
          T,
          N,
          C,
          $,
          L,
          I
        );
        return;
      }
    }
    X & 8 ? (Y & 16 && os(A, N, C), B !== A && f(E, B)) : Y & 16 ? X & 16 ? ee(
      A,
      B,
      E,
      T,
      N,
      C,
      $,
      L,
      I
    ) : os(A, N, C, !0) : (Y & 8 && f(E, ""), X & 16 && D(
      B,
      E,
      T,
      N,
      C,
      $,
      L,
      I
    ));
  }, re = (m, _, E, T, N, C, $, L, I) => {
    m = m || Wn, _ = _ || Wn;
    const A = m.length, Y = _.length, B = Math.min(A, Y);
    let H;
    for (H = 0; H < B; H++) {
      const X = _[H] = I ? Ze(_[H]) : ce(_[H]);
      g(
        m[H],
        X,
        E,
        null,
        N,
        C,
        $,
        L,
        I
      );
    }
    A > Y ? os(
      m,
      N,
      C,
      !0,
      !1,
      B
    ) : D(
      _,
      E,
      T,
      N,
      C,
      $,
      L,
      I,
      B
    );
  }, ee = (m, _, E, T, N, C, $, L, I) => {
    let A = 0;
    const Y = _.length;
    let B = m.length - 1, H = Y - 1;
    for (; A <= B && A <= H; ) {
      const X = m[A], rt = _[A] = I ? Ze(_[A]) : ce(_[A]);
      if (us(X, rt))
        g(
          X,
          rt,
          E,
          null,
          N,
          C,
          $,
          L,
          I
        );
      else
        break;
      A++;
    }
    for (; A <= B && A <= H; ) {
      const X = m[B], rt = _[H] = I ? Ze(_[H]) : ce(_[H]);
      if (us(X, rt))
        g(
          X,
          rt,
          E,
          null,
          N,
          C,
          $,
          L,
          I
        );
      else
        break;
      B--, H--;
    }
    if (A > B) {
      if (A <= H) {
        const X = H + 1, rt = X < Y ? _[X].el : T;
        for (; A <= H; )
          g(
            null,
            _[A] = I ? Ze(_[A]) : ce(_[A]),
            E,
            rt,
            N,
            C,
            $,
            L,
            I
          ), A++;
      }
    } else if (A > H)
      for (; A <= B; )
        Nt(m[A], N, C, !0), A++;
    else {
      const X = A, rt = A, pt = /* @__PURE__ */ new Map();
      for (A = rt; A <= H; A++) {
        const Lt = _[A] = I ? Ze(_[A]) : ce(_[A]);
        Lt.key != null && (x.NODE_ENV !== "production" && pt.has(Lt.key) && R(
          "Duplicate keys found during update:",
          JSON.stringify(Lt.key),
          "Make sure keys are unique."
        ), pt.set(Lt.key, A));
      }
      let ct, Xt = 0;
      const zt = H - rt + 1;
      let me = !1, be = 0;
      const as = new Array(zt);
      for (A = 0; A < zt; A++) as[A] = 0;
      for (A = X; A <= B; A++) {
        const Lt = m[A];
        if (Xt >= zt) {
          Nt(Lt, N, C, !0);
          continue;
        }
        let _e;
        if (Lt.key != null)
          _e = pt.get(Lt.key);
        else
          for (ct = rt; ct <= H; ct++)
            if (as[ct - rt] === 0 && us(Lt, _[ct])) {
              _e = ct;
              break;
            }
        _e === void 0 ? Nt(Lt, N, C, !0) : (as[_e - rt] = A + 1, _e >= be ? be = _e : me = !0, g(
          Lt,
          _[_e],
          E,
          null,
          N,
          C,
          $,
          L,
          I
        ), Xt++);
      }
      const Aa = me ? Xp(as) : Wn;
      for (ct = Aa.length - 1, A = zt - 1; A >= 0; A--) {
        const Lt = rt + A, _e = _[Lt], Va = Lt + 1 < Y ? _[Lt + 1].el : T;
        as[A] === 0 ? g(
          null,
          _e,
          E,
          Va,
          N,
          C,
          $,
          L,
          I
        ) : me && (ct < 0 || A !== Aa[ct] ? It(_e, E, Va, 2) : ct--);
      }
    }
  }, It = (m, _, E, T, N = null) => {
    const { el: C, type: $, transition: L, children: I, shapeFlag: A } = m;
    if (A & 6) {
      It(m.component.subTree, _, E, T);
      return;
    }
    if (A & 128) {
      m.suspense.move(_, E, T);
      return;
    }
    if (A & 64) {
      $.move(m, _, E, rs);
      return;
    }
    if ($ === le) {
      s(C, _, E);
      for (let B = 0; B < I.length; B++)
        It(I[B], _, E, T);
      s(m.anchor, _, E);
      return;
    }
    if ($ === Ni) {
      P(m, _, E);
      return;
    }
    if (T !== 2 && A & 1 && L)
      if (T === 0)
        L.beforeEnter(C), s(C, _, E), Bt(() => L.enter(C), N);
      else {
        const { leave: B, delayLeave: H, afterLeave: X } = L, rt = () => s(C, _, E), pt = () => {
          B(C, () => {
            rt(), X && X();
          });
        };
        H ? H(C, rt, pt) : pt();
      }
    else
      s(C, _, E);
  }, Nt = (m, _, E, T = !1, N = !1) => {
    const {
      type: C,
      props: $,
      ref: L,
      children: I,
      dynamicChildren: A,
      shapeFlag: Y,
      patchFlag: B,
      dirs: H,
      cacheIndex: X
    } = m;
    if (B === -2 && (N = !1), L != null && Hi(L, null, E, m, !0), X != null && (_.renderCache[X] = void 0), Y & 256) {
      _.ctx.deactivate(m);
      return;
    }
    const rt = Y & 1 && H, pt = !Ms(m);
    let ct;
    if (pt && (ct = $ && $.onVnodeBeforeUnmount) && ye(ct, _, m), Y & 6)
      Re(m.component, E, T);
    else {
      if (Y & 128) {
        m.suspense.unmount(E, T);
        return;
      }
      rt && hn(m, null, _, "beforeUnmount"), Y & 64 ? m.type.remove(
        m,
        _,
        E,
        rs,
        T
      ) : A && // #5154
      // when v-once is used inside a block, setBlockTracking(-1) marks the
      // parent block with hasOnce: true
      // so that it doesn't take the fast path during unmount - otherwise
      // components nested in v-once are never unmounted.
      !A.hasOnce && // #1153: fast path should not be taken for non-stable (v-for) fragments
      (C !== le || B > 0 && B & 64) ? os(
        A,
        _,
        E,
        !1,
        !0
      ) : (C === le && B & 384 || !N && Y & 16) && os(I, _, E), T && ae(m);
    }
    (pt && (ct = $ && $.onVnodeUnmounted) || rt) && Bt(() => {
      ct && ye(ct, _, m), rt && hn(m, null, _, "unmounted");
    }, E);
  }, ae = (m) => {
    const { type: _, el: E, anchor: T, transition: N } = m;
    if (_ === le) {
      x.NODE_ENV !== "production" && m.patchFlag > 0 && m.patchFlag & 2048 && N && !N.persisted ? m.children.forEach(($) => {
        $.type === te ? i($.el) : ae($);
      }) : un(E, T);
      return;
    }
    if (_ === Ni) {
      w(m);
      return;
    }
    const C = () => {
      i(E), N && !N.persisted && N.afterLeave && N.afterLeave();
    };
    if (m.shapeFlag & 1 && N && !N.persisted) {
      const { leave: $, delayLeave: L } = N, I = () => $(E, C);
      L ? L(m.el, C, I) : I();
    } else
      C();
  }, un = (m, _) => {
    let E;
    for (; m !== _; )
      E = h(m), i(m), m = E;
    i(_);
  }, Re = (m, _, E) => {
    x.NODE_ENV !== "production" && m.type.__hmrId && Hd(m);
    const { bum: T, scope: N, job: C, subTree: $, um: L, m: I, a: A } = m;
    Ja(I), Ja(A), T && ls(T), N.stop(), C && (C.flags |= 8, Nt($, m, _, E)), L && Bt(L, _), Bt(() => {
      m.isUnmounted = !0;
    }, _), _ && _.pendingBranch && !_.isUnmounted && m.asyncDep && !m.asyncResolved && m.suspenseId === _.pendingId && (_.deps--, _.deps === 0 && _.resolve()), x.NODE_ENV !== "production" && Gd(m);
  }, os = (m, _, E, T = !1, N = !1, C = 0) => {
    for (let $ = C; $ < m.length; $++)
      Nt(m[$], _, E, T, N);
  }, Js = (m) => {
    if (m.shapeFlag & 6)
      return Js(m.component.subTree);
    if (m.shapeFlag & 128)
      return m.suspense.next();
    const _ = h(m.anchor || m.el), E = _ && _[Bf];
    return E ? h(E) : _;
  };
  let Oo = !1;
  const Ta = (m, _, E) => {
    m == null ? _._vnode && Nt(_._vnode, null, null, !0) : g(
      _._vnode || null,
      m,
      _,
      null,
      null,
      null,
      E
    ), _._vnode = m, Oo || (Oo = !0, Ba(), Tf(), Oo = !1);
  }, rs = {
    p: g,
    um: Nt,
    m: It,
    r: ae,
    mt: it,
    mc: D,
    pc: Ct,
    pbc: z,
    n: Js,
    o: e
  };
  return {
    render: Ta,
    hydrate: void 0,
    createApp: Cp(Ta)
  };
}
function To({ type: e, props: t }, n) {
  return n === "svg" && e === "foreignObject" || n === "mathml" && e === "annotation-xml" && t && t.encoding && t.encoding.includes("html") ? void 0 : n;
}
function dn({ effect: e, job: t }, n) {
  n ? (e.flags |= 32, t.flags |= 4) : (e.flags &= -33, t.flags &= -5);
}
function qp(e, t) {
  return (!e || e && !e.pendingBranch) && t && !t.persisted;
}
function ks(e, t, n = !1) {
  const s = e.children, i = t.children;
  if (U(s) && U(i))
    for (let o = 0; o < s.length; o++) {
      const r = s[o];
      let a = i[o];
      a.shapeFlag & 1 && !a.dynamicChildren && ((a.patchFlag <= 0 || a.patchFlag === 32) && (a = i[o] = Ze(i[o]), a.el = r.el), !n && a.patchFlag !== -2 && ks(r, a)), a.type === Xs && (a.el = r.el), x.NODE_ENV !== "production" && a.type === te && !a.el && (a.el = r.el);
    }
}
function Xp(e) {
  const t = e.slice(), n = [0];
  let s, i, o, r, a;
  const l = e.length;
  for (s = 0; s < l; s++) {
    const c = e[s];
    if (c !== 0) {
      if (i = n[n.length - 1], e[i] < c) {
        t[s] = i, n.push(s);
        continue;
      }
      for (o = 0, r = n.length - 1; o < r; )
        a = o + r >> 1, e[n[a]] < c ? o = a + 1 : r = a;
      c < e[n[o]] && (o > 0 && (t[s] = n[o - 1]), n[o] = s);
    }
  }
  for (o = n.length, r = n[o - 1]; o-- > 0; )
    n[o] = r, r = t[r];
  return n;
}
function ou(e) {
  const t = e.subTree.component;
  if (t)
    return t.asyncDep && !t.asyncResolved ? t : ou(t);
}
function Ja(e) {
  if (e)
    for (let t = 0; t < e.length; t++)
      e[t].flags |= 8;
}
const Gp = Symbol.for("v-scx"), Zp = () => {
  {
    const e = ki(Gp);
    return e || x.NODE_ENV !== "production" && R(
      "Server rendering context not provided. Make sure to only call useSSRContext() conditionally in the server build."
    ), e;
  }
};
function Ao(e, t, n) {
  return x.NODE_ENV !== "production" && !K(t) && R(
    "`watch(fn, options?)` signature has been moved to a separate API. Use `watchEffect(fn, options?)` instead. `watch` now only supports `watch(source, cb, options?) signature."
  ), ru(e, t, n);
}
function ru(e, t, n = ut) {
  const { immediate: s, deep: i, flush: o, once: r } = n;
  x.NODE_ENV !== "production" && !t && (s !== void 0 && R(
    'watch() "immediate" option is only respected when using the watch(source, callback, options?) signature.'
  ), i !== void 0 && R(
    'watch() "deep" option is only respected when using the watch(source, callback, options?) signature.'
  ), r !== void 0 && R(
    'watch() "once" option is only respected when using the watch(source, callback, options?) signature.'
  ));
  const a = _t({}, n);
  x.NODE_ENV !== "production" && (a.onWarn = R);
  const l = t && s || !t && o !== "post";
  let c;
  if ($s) {
    if (o === "sync") {
      const d = Zp();
      c = d.__watcherHandles || (d.__watcherHandles = []);
    } else if (!l) {
      const d = () => {
      };
      return d.stop = St, d.resume = St, d.pause = St, d;
    }
  }
  const f = Dt;
  a.call = (d, p, g) => Ve(d, f, p, g);
  let u = !1;
  o === "post" ? a.scheduler = (d) => {
    Bt(d, f && f.suspense);
  } : o !== "sync" && (u = !0, a.scheduler = (d, p) => {
    p ? d() : po(d);
  }), a.augmentJob = (d) => {
    t && (d.flags |= 4), u && (d.flags |= 2, f && (d.id = f.uid, d.i = f));
  };
  const h = Vd(e, t, a);
  return $s && (c ? c.push(h) : l && h()), h;
}
function Jp(e, t, n) {
  const s = this.proxy, i = bt(e) ? e.includes(".") ? au(s, e) : () => s[e] : e.bind(s, s);
  let o;
  K(t) ? o = t : (o = t.handler, n = t);
  const r = Gs(this), a = ru(i, o.bind(s), n);
  return r(), a;
}
function au(e, t) {
  const n = t.split(".");
  return () => {
    let s = e;
    for (let i = 0; i < n.length && s; i++)
      s = s[n[i]];
    return s;
  };
}
const Qp = (e, t) => t === "modelValue" || t === "model-value" ? e.modelModifiers : e[`${t}Modifiers`] || e[`${Kt(t)}Modifiers`] || e[`${Zt(t)}Modifiers`];
function tg(e, t, ...n) {
  if (e.isUnmounted) return;
  const s = e.vnode.props || ut;
  if (x.NODE_ENV !== "production") {
    const {
      emitsOptions: f,
      propsOptions: [u]
    } = e;
    if (f)
      if (!(t in f))
        (!u || !(bn(Kt(t)) in u)) && R(
          `Component emitted event "${t}" but it is neither declared in the emits option nor as an "${bn(Kt(t))}" prop.`
        );
      else {
        const h = f[t];
        K(h) && (h(...n) || R(
          `Invalid event arguments: event validation failed for event "${t}".`
        ));
      }
  }
  let i = n;
  const o = t.startsWith("update:"), r = o && Qp(s, t.slice(7));
  if (r && (r.trim && (i = n.map((f) => bt(f) ? f.trim() : f)), r.number && (i = n.map(Xh))), x.NODE_ENV !== "production" && Qd(e, t, i), x.NODE_ENV !== "production") {
    const f = t.toLowerCase();
    f !== t && s[bn(f)] && R(
      `Event "${f}" is emitted in component ${_o(
        e,
        e.type
      )} but the handler is registered for "${t}". Note that HTML attributes are case-insensitive and you cannot use v-on to listen to camelCase events when using in-DOM templates. You should probably use "${Zt(
        t
      )}" instead of "${t}".`
    );
  }
  let a, l = s[a = bn(t)] || // also try camelCase event handler (#2249)
  s[a = bn(Kt(t))];
  !l && o && (l = s[a = bn(Zt(t))]), l && Ve(
    l,
    e,
    6,
    i
  );
  const c = s[a + "Once"];
  if (c) {
    if (!e.emitted)
      e.emitted = {};
    else if (e.emitted[a])
      return;
    e.emitted[a] = !0, Ve(
      c,
      e,
      6,
      i
    );
  }
}
function lu(e, t, n = !1) {
  const s = t.emitsCache, i = s.get(e);
  if (i !== void 0)
    return i;
  const o = e.emits;
  let r = {}, a = !1;
  if (!K(e)) {
    const l = (c) => {
      const f = lu(c, t, !0);
      f && (a = !0, _t(r, f));
    };
    !n && t.mixins.length && t.mixins.forEach(l), e.extends && l(e.extends), e.mixins && e.mixins.forEach(l);
  }
  return !o && !a ? (dt(e) && s.set(e, null), null) : (U(o) ? o.forEach((l) => r[l] = null) : _t(r, o), dt(e) && s.set(e, r), r);
}
function mo(e, t) {
  return !e || !Us(t) ? !1 : (t = t.slice(2).replace(/Once$/, ""), at(e, t[0].toLowerCase() + t.slice(1)) || at(e, Zt(t)) || at(e, t));
}
let xr = !1;
function Yi() {
  xr = !0;
}
function Qa(e) {
  const {
    type: t,
    vnode: n,
    proxy: s,
    withProxy: i,
    propsOptions: [o],
    slots: r,
    attrs: a,
    emit: l,
    render: c,
    renderCache: f,
    props: u,
    data: h,
    setupState: d,
    ctx: p,
    inheritAttrs: g
  } = e, b = zi(e);
  let y, O;
  x.NODE_ENV !== "production" && (xr = !1);
  try {
    if (n.shapeFlag & 4) {
      const w = i || s, k = x.NODE_ENV !== "production" && d.__isScriptSetup ? new Proxy(w, {
        get(v, S, D) {
          return R(
            `Property '${String(
              S
            )}' was accessed via 'this'. Avoid using 'this' in templates.`
          ), Reflect.get(v, S, D);
        }
      }) : w;
      y = ce(
        c.call(
          k,
          w,
          f,
          x.NODE_ENV !== "production" ? ke(u) : u,
          d,
          h,
          p
        )
      ), O = a;
    } else {
      const w = t;
      x.NODE_ENV !== "production" && a === u && Yi(), y = ce(
        w.length > 1 ? w(
          x.NODE_ENV !== "production" ? ke(u) : u,
          x.NODE_ENV !== "production" ? {
            get attrs() {
              return Yi(), ke(a);
            },
            slots: r,
            emit: l
          } : { attrs: a, slots: r, emit: l }
        ) : w(
          x.NODE_ENV !== "production" ? ke(u) : u,
          null
        )
      ), O = t.props ? a : eg(a);
    }
  } catch (w) {
    Ns.length = 0, Ks(w, e, 1), y = De(te);
  }
  let M = y, P;
  if (x.NODE_ENV !== "production" && y.patchFlag > 0 && y.patchFlag & 2048 && ([M, P] = cu(y)), O && g !== !1) {
    const w = Object.keys(O), { shapeFlag: k } = M;
    if (w.length) {
      if (k & 7)
        o && w.some(Ii) && (O = ng(
          O,
          o
        )), M = on(M, O, !1, !0);
      else if (x.NODE_ENV !== "production" && !xr && M.type !== te) {
        const v = Object.keys(a), S = [], D = [];
        for (let F = 0, z = v.length; F < z; F++) {
          const j = v[F];
          Us(j) ? Ii(j) || S.push(j[2].toLowerCase() + j.slice(3)) : D.push(j);
        }
        D.length && R(
          `Extraneous non-props attributes (${D.join(", ")}) were passed to component but could not be automatically inherited because component renders fragment or text or teleport root nodes.`
        ), S.length && R(
          `Extraneous non-emits event listeners (${S.join(", ")}) were passed to component but could not be automatically inherited because component renders fragment or text root nodes. If the listener is intended to be a component custom event listener only, declare it using the "emits" option.`
        );
      }
    }
  }
  return n.dirs && (x.NODE_ENV !== "production" && !tl(M) && R(
    "Runtime directive used on component with non-element root node. The directives will not function as intended."
  ), M = on(M, null, !1, !0), M.dirs = M.dirs ? M.dirs.concat(n.dirs) : n.dirs), n.transition && (x.NODE_ENV !== "production" && !tl(M) && R(
    "Component inside <Transition> renders non-element root node that cannot be animated."
  ), ta(M, n.transition)), x.NODE_ENV !== "production" && P ? P(M) : y = M, zi(b), y;
}
const cu = (e) => {
  const t = e.children, n = e.dynamicChildren, s = ia(t, !1);
  if (s) {
    if (x.NODE_ENV !== "production" && s.patchFlag > 0 && s.patchFlag & 2048)
      return cu(s);
  } else return [e, void 0];
  const i = t.indexOf(s), o = n ? n.indexOf(s) : -1, r = (a) => {
    t[i] = a, n && (o > -1 ? n[o] = a : a.patchFlag > 0 && (e.dynamicChildren = [...n, a]));
  };
  return [ce(s), r];
};
function ia(e, t = !0) {
  let n;
  for (let s = 0; s < e.length; s++) {
    const i = e[s];
    if (bo(i)) {
      if (i.type !== te || i.children === "v-if") {
        if (n)
          return;
        if (n = i, x.NODE_ENV !== "production" && t && n.patchFlag > 0 && n.patchFlag & 2048)
          return ia(n.children);
      }
    } else
      return;
  }
  return n;
}
const eg = (e) => {
  let t;
  for (const n in e)
    (n === "class" || n === "style" || Us(n)) && ((t || (t = {}))[n] = e[n]);
  return t;
}, ng = (e, t) => {
  const n = {};
  for (const s in e)
    (!Ii(s) || !(s.slice(9) in t)) && (n[s] = e[s]);
  return n;
}, tl = (e) => e.shapeFlag & 7 || e.type === te;
function sg(e, t, n) {
  const { props: s, children: i, component: o } = e, { props: r, children: a, patchFlag: l } = t, c = o.emitsOptions;
  if (x.NODE_ENV !== "production" && (i || a) && fe || t.dirs || t.transition)
    return !0;
  if (n && l >= 0) {
    if (l & 1024)
      return !0;
    if (l & 16)
      return s ? el(s, r, c) : !!r;
    if (l & 8) {
      const f = t.dynamicProps;
      for (let u = 0; u < f.length; u++) {
        const h = f[u];
        if (r[h] !== s[h] && !mo(c, h))
          return !0;
      }
    }
  } else
    return (i || a) && (!a || !a.$stable) ? !0 : s === r ? !1 : s ? r ? el(s, r, c) : !0 : !!r;
  return !1;
}
function el(e, t, n) {
  const s = Object.keys(t);
  if (s.length !== Object.keys(e).length)
    return !0;
  for (let i = 0; i < s.length; i++) {
    const o = s[i];
    if (t[o] !== e[o] && !mo(n, o))
      return !0;
  }
  return !1;
}
function ig({ vnode: e, parent: t }, n) {
  for (; t; ) {
    const s = t.subTree;
    if (s.suspense && s.suspense.activeBranch === e && (s.el = e.el), s === e)
      (e = t.vnode).el = n, t = t.parent;
    else
      break;
  }
}
const fu = (e) => e.__isSuspense;
function og(e, t) {
  t && t.pendingBranch ? U(e) ? t.effects.push(...e) : t.effects.push(e) : Pf(e);
}
const le = Symbol.for("v-fgt"), Xs = Symbol.for("v-txt"), te = Symbol.for("v-cmt"), Ni = Symbol.for("v-stc"), Ns = [];
let Qt = null;
function ys(e = !1) {
  Ns.push(Qt = e ? null : []);
}
function rg() {
  Ns.pop(), Qt = Ns[Ns.length - 1] || null;
}
let Fs = 1;
function nl(e, t = !1) {
  Fs += e, e < 0 && Qt && t && (Qt.hasOnce = !0);
}
function uu(e) {
  return e.dynamicChildren = Fs > 0 ? Qt || Wn : null, rg(), Fs > 0 && Qt && Qt.push(e), e;
}
function Vo(e, t, n, s, i, o) {
  return uu(
    Wt(
      e,
      t,
      n,
      s,
      i,
      o,
      !0
    )
  );
}
function hu(e, t, n, s, i) {
  return uu(
    De(
      e,
      t,
      n,
      s,
      i,
      !0
    )
  );
}
function bo(e) {
  return e ? e.__v_isVNode === !0 : !1;
}
function us(e, t) {
  if (x.NODE_ENV !== "production" && t.shapeFlag & 6 && e.component) {
    const n = Si.get(t.type);
    if (n && n.has(e.component))
      return e.shapeFlag &= -257, t.shapeFlag &= -513, !1;
  }
  return e.type === t.type && e.key === t.key;
}
const ag = (...e) => pu(
  ...e
), du = ({ key: e }) => e ?? null, Di = ({
  ref: e,
  ref_key: t,
  ref_for: n
}) => (typeof e == "number" && (e = "" + e), e != null ? bt(e) || kt(e) || K(e) ? { i: Jt, r: e, k: t, f: !!n } : e : null);
function Wt(e, t = null, n = null, s = 0, i = null, o = e === le ? 0 : 1, r = !1, a = !1) {
  const l = {
    __v_isVNode: !0,
    __v_skip: !0,
    type: e,
    props: t,
    key: t && du(t),
    ref: t && Di(t),
    scopeId: Ff,
    slotScopeIds: null,
    children: n,
    component: null,
    suspense: null,
    ssContent: null,
    ssFallback: null,
    dirs: null,
    transition: null,
    el: null,
    anchor: null,
    target: null,
    targetStart: null,
    targetAnchor: null,
    staticCount: 0,
    shapeFlag: o,
    patchFlag: s,
    dynamicProps: i,
    dynamicChildren: null,
    appContext: null,
    ctx: Jt
  };
  return a ? (oa(l, n), o & 128 && e.normalize(l)) : n && (l.shapeFlag |= bt(n) ? 8 : 16), x.NODE_ENV !== "production" && l.key !== l.key && R("VNode created with invalid key (NaN). VNode type:", l.type), Fs > 0 && // avoid a block node from tracking itself
  !r && // has current parent block
  Qt && // presence of a patch flag indicates this node needs patching on updates.
  // component nodes also should always be patched, because even if the
  // component doesn't need to update, it needs to persist the instance on to
  // the next vnode so that it can be properly unmounted later.
  (l.patchFlag > 0 || o & 6) && // the EVENTS flag is only for hydration and if it is the only flag, the
  // vnode should not be considered dynamic due to handler caching.
  l.patchFlag !== 32 && Qt.push(l), l;
}
const De = x.NODE_ENV !== "production" ? ag : pu;
function pu(e, t = null, n = null, s = 0, i = null, o = !1) {
  if ((!e || e === _p) && (x.NODE_ENV !== "production" && !e && R(`Invalid vnode type when creating vnode: ${e}.`), e = te), bo(e)) {
    const a = on(
      e,
      t,
      !0
      /* mergeRef: true */
    );
    return n && oa(a, n), Fs > 0 && !o && Qt && (a.shapeFlag & 6 ? Qt[Qt.indexOf(e)] = a : Qt.push(a)), a.patchFlag = -2, a;
  }
  if (yu(e) && (e = e.__vccOpts), t) {
    t = lg(t);
    let { class: a, style: l } = t;
    a && !bt(a) && (t.class = Yr(a)), dt(l) && (Fi(l) && !U(l) && (l = _t({}, l)), t.style = co(l));
  }
  const r = bt(e) ? 1 : fu(e) ? 128 : ep(e) ? 64 : dt(e) ? 4 : K(e) ? 2 : 0;
  return x.NODE_ENV !== "production" && r & 4 && Fi(e) && (e = et(e), R(
    "Vue received a Component that was made a reactive object. This can lead to unnecessary performance overhead and should be avoided by marking the component with `markRaw` or using `shallowRef` instead of `ref`.",
    `
Component that was made reactive: `,
    e
  )), Wt(
    e,
    t,
    n,
    s,
    i,
    r,
    o,
    !0
  );
}
function lg(e) {
  return e ? Fi(e) || Jf(e) ? _t({}, e) : e : null;
}
function on(e, t, n = !1, s = !1) {
  const { props: i, ref: o, patchFlag: r, children: a, transition: l } = e, c = t ? ug(i || {}, t) : i, f = {
    __v_isVNode: !0,
    __v_skip: !0,
    type: e.type,
    props: c,
    key: c && du(c),
    ref: t && t.ref ? (
      // #2078 in the case of <component :is="vnode" ref="extra"/>
      // if the vnode itself already has a ref, cloneVNode will need to merge
      // the refs so the single vnode can be set on multiple refs
      n && o ? U(o) ? o.concat(Di(t)) : [o, Di(t)] : Di(t)
    ) : o,
    scopeId: e.scopeId,
    slotScopeIds: e.slotScopeIds,
    children: x.NODE_ENV !== "production" && r === -1 && U(a) ? a.map(gu) : a,
    target: e.target,
    targetStart: e.targetStart,
    targetAnchor: e.targetAnchor,
    staticCount: e.staticCount,
    shapeFlag: e.shapeFlag,
    // if the vnode is cloned with extra props, we can no longer assume its
    // existing patch flag to be reliable and need to add the FULL_PROPS flag.
    // note: preserve flag for fragments since they use the flag for children
    // fast paths only.
    patchFlag: t && e.type !== le ? r === -1 ? 16 : r | 16 : r,
    dynamicProps: e.dynamicProps,
    dynamicChildren: e.dynamicChildren,
    appContext: e.appContext,
    dirs: e.dirs,
    transition: l,
    // These should technically only be non-null on mounted VNodes. However,
    // they *should* be copied for kept-alive vnodes. So we just always copy
    // them since them being non-null during a mount doesn't affect the logic as
    // they will simply be overwritten.
    component: e.component,
    suspense: e.suspense,
    ssContent: e.ssContent && on(e.ssContent),
    ssFallback: e.ssFallback && on(e.ssFallback),
    el: e.el,
    anchor: e.anchor,
    ctx: e.ctx,
    ce: e.ce
  };
  return l && s && ta(
    f,
    l.clone(f)
  ), f;
}
function gu(e) {
  const t = on(e);
  return U(e.children) && (t.children = e.children.map(gu)), t;
}
function cg(e = " ", t = 0) {
  return De(Xs, null, e, t);
}
function fg(e = "", t = !1) {
  return t ? (ys(), hu(te, null, e)) : De(te, null, e);
}
function ce(e) {
  return e == null || typeof e == "boolean" ? De(te) : U(e) ? De(
    le,
    null,
    // #3666, avoid reference pollution when reusing vnode
    e.slice()
  ) : bo(e) ? Ze(e) : De(Xs, null, String(e));
}
function Ze(e) {
  return e.el === null && e.patchFlag !== -1 || e.memo ? e : on(e);
}
function oa(e, t) {
  let n = 0;
  const { shapeFlag: s } = e;
  if (t == null)
    t = null;
  else if (U(t))
    n = 16;
  else if (typeof t == "object")
    if (s & 65) {
      const i = t.default;
      i && (i._c && (i._d = !1), oa(e, i()), i._c && (i._d = !0));
      return;
    } else {
      n = 32;
      const i = t._;
      !i && !Jf(t) ? t._ctx = Jt : i === 3 && Jt && (Jt.slots._ === 1 ? t._ = 1 : (t._ = 2, e.patchFlag |= 1024));
    }
  else K(t) ? (t = { default: t, _ctx: Jt }, n = 32) : (t = String(t), s & 64 ? (n = 16, t = [cg(t)]) : n = 8);
  e.children = t, e.shapeFlag |= n;
}
function ug(...e) {
  const t = {};
  for (let n = 0; n < e.length; n++) {
    const s = e[n];
    for (const i in s)
      if (i === "class")
        t.class !== s.class && (t.class = Yr([t.class, s.class]));
      else if (i === "style")
        t.style = co([t.style, s.style]);
      else if (Us(i)) {
        const o = t[i], r = s[i];
        r && o !== r && !(U(o) && o.includes(r)) && (t[i] = o ? [].concat(o, r) : r);
      } else i !== "" && (t[i] = s[i]);
  }
  return t;
}
function ye(e, t, n, s = null) {
  Ve(e, t, 7, [
    n,
    s
  ]);
}
const hg = Xf();
let dg = 0;
function pg(e, t, n) {
  const s = e.type, i = (t ? t.appContext : e.appContext) || hg, o = {
    uid: dg++,
    vnode: e,
    type: s,
    parent: t,
    appContext: i,
    root: null,
    // to be immediately set
    next: null,
    subTree: null,
    // will be set synchronously right after creation
    effect: null,
    update: null,
    // will be set synchronously right after creation
    job: null,
    scope: new ld(
      !0
      /* detached */
    ),
    render: null,
    proxy: null,
    exposed: null,
    exposeProxy: null,
    withProxy: null,
    provides: t ? t.provides : Object.create(i.provides),
    ids: t ? t.ids : ["", 0, 0],
    accessCache: null,
    renderCache: [],
    // local resolved assets
    components: null,
    directives: null,
    // resolved props and emits options
    propsOptions: tu(s, i),
    emitsOptions: lu(s, i),
    // emit
    emit: null,
    // to be set immediately
    emitted: null,
    // props default value
    propsDefaults: ut,
    // inheritAttrs
    inheritAttrs: s.inheritAttrs,
    // state
    ctx: ut,
    data: ut,
    props: ut,
    attrs: ut,
    slots: ut,
    refs: ut,
    setupState: ut,
    setupContext: null,
    // suspense related
    suspense: n,
    suspenseId: n ? n.pendingId : 0,
    asyncDep: null,
    asyncResolved: !1,
    // lifecycle hooks
    // not using enums here because it results in computed properties
    isMounted: !1,
    isUnmounted: !1,
    isDeactivated: !1,
    bc: null,
    c: null,
    bm: null,
    m: null,
    bu: null,
    u: null,
    um: null,
    bum: null,
    da: null,
    a: null,
    rtg: null,
    rtc: null,
    ec: null,
    sp: null
  };
  return x.NODE_ENV !== "production" ? o.ctx = xp(o) : o.ctx = { _: o }, o.root = t ? t.root : o, o.emit = tg.bind(null, o), e.ce && e.ce(o), o;
}
let Dt = null;
const gg = () => Dt || Jt;
let Ki, vr;
{
  const e = Ys(), t = (n, s) => {
    let i;
    return (i = e[n]) || (i = e[n] = []), i.push(s), (o) => {
      i.length > 1 ? i.forEach((r) => r(o)) : i[0](o);
    };
  };
  Ki = t(
    "__VUE_INSTANCE_SETTERS__",
    (n) => Dt = n
  ), vr = t(
    "__VUE_SSR_SETTERS__",
    (n) => $s = n
  );
}
const Gs = (e) => {
  const t = Dt;
  return Ki(e), e.scope.on(), () => {
    e.scope.off(), Ki(t);
  };
}, sl = () => {
  Dt && Dt.scope.off(), Ki(null);
}, mg = /* @__PURE__ */ Ye("slot,component");
function wr(e, { isNativeTag: t }) {
  (mg(e) || t(e)) && R(
    "Do not use built-in or reserved HTML elements as component id: " + e
  );
}
function mu(e) {
  return e.vnode.shapeFlag & 4;
}
let $s = !1;
function bg(e, t = !1, n = !1) {
  t && vr(t);
  const { props: s, children: i } = e.vnode, o = mu(e);
  Tp(e, s, o, t), Hp(e, i, n);
  const r = o ? _g(e, t) : void 0;
  return t && vr(!1), r;
}
function _g(e, t) {
  var n;
  const s = e.type;
  if (x.NODE_ENV !== "production") {
    if (s.name && wr(s.name, e.appContext.config), s.components) {
      const o = Object.keys(s.components);
      for (let r = 0; r < o.length; r++)
        wr(o[r], e.appContext.config);
    }
    if (s.directives) {
      const o = Object.keys(s.directives);
      for (let r = 0; r < o.length; r++)
        $f(o[r]);
    }
    s.compilerOptions && yg() && R(
      '"compilerOptions" is only supported when using a build of Vue that includes the runtime compiler. Since you are using a runtime-only build, the options should be passed via your build tool config instead.'
    );
  }
  e.accessCache = /* @__PURE__ */ Object.create(null), e.proxy = new Proxy(e.ctx, Yf), x.NODE_ENV !== "production" && vp(e);
  const { setup: i } = s;
  if (i) {
    Ke();
    const o = e.setupContext = i.length > 1 ? vg(e) : null, r = Gs(e), a = Jn(
      i,
      e,
      0,
      [
        x.NODE_ENV !== "production" ? ke(e.props) : e.props,
        o
      ]
    ), l = Hr(a);
    if (qe(), r(), (l || e.sp) && !Ms(e) && Hf(e), l) {
      if (a.then(sl, sl), t)
        return a.then((c) => {
          il(e, c, t);
        }).catch((c) => {
          Ks(c, e, 0);
        });
      if (e.asyncDep = a, x.NODE_ENV !== "production" && !e.suspense) {
        const c = (n = s.name) != null ? n : "Anonymous";
        R(
          `Component <${c}>: setup function returned a promise, but no <Suspense> boundary was found in the parent component tree. A component with async setup() must be nested in a <Suspense> in order to be rendered.`
        );
      }
    } else
      il(e, a, t);
  } else
    bu(e, t);
}
function il(e, t, n) {
  K(t) ? e.type.__ssrInlineRender ? e.ssrRender = t : e.render = t : dt(t) ? (x.NODE_ENV !== "production" && bo(t) && R(
    "setup() should not return VNodes directly - return a render function instead."
  ), x.NODE_ENV !== "production" && (e.devtoolsRawSetupState = t), e.setupState = Mf(t), x.NODE_ENV !== "production" && wp(e)) : x.NODE_ENV !== "production" && t !== void 0 && R(
    `setup() should return an object. Received: ${t === null ? "null" : typeof t}`
  ), bu(e, n);
}
const yg = () => !0;
function bu(e, t, n) {
  const s = e.type;
  e.render || (e.render = s.render || St);
  {
    const i = Gs(e);
    Ke();
    try {
      Op(e);
    } finally {
      qe(), i();
    }
  }
  x.NODE_ENV !== "production" && !s.render && e.render === St && !t && (s.template ? R(
    'Component provided template option but runtime compilation is not supported in this build of Vue. Configure your bundler to alias "vue" to "vue/dist/vue.esm-bundler.js".'
  ) : R("Component is missing template or render function: ", s));
}
const ol = x.NODE_ENV !== "production" ? {
  get(e, t) {
    return Yi(), Ot(e, "get", ""), e[t];
  },
  set() {
    return R("setupContext.attrs is readonly."), !1;
  },
  deleteProperty() {
    return R("setupContext.attrs is readonly."), !1;
  }
} : {
  get(e, t) {
    return Ot(e, "get", ""), e[t];
  }
};
function xg(e) {
  return new Proxy(e.slots, {
    get(t, n) {
      return Ot(e, "get", "$slots"), t[n];
    }
  });
}
function vg(e) {
  const t = (n) => {
    if (x.NODE_ENV !== "production" && (e.exposed && R("expose() should be called only once per setup()."), n != null)) {
      let s = typeof n;
      s === "object" && (U(n) ? s = "array" : kt(n) && (s = "ref")), s !== "object" && R(
        `expose() should be passed a plain object, received ${s}.`
      );
    }
    e.exposed = n || {};
  };
  if (x.NODE_ENV !== "production") {
    let n, s;
    return Object.freeze({
      get attrs() {
        return n || (n = new Proxy(e.attrs, ol));
      },
      get slots() {
        return s || (s = xg(e));
      },
      get emit() {
        return (i, ...o) => e.emit(i, ...o);
      },
      expose: t
    });
  } else
    return {
      attrs: new Proxy(e.attrs, ol),
      slots: e.slots,
      emit: e.emit,
      expose: t
    };
}
function ra(e) {
  return e.exposed ? e.exposeProxy || (e.exposeProxy = new Proxy(Mf(Dd(e.exposed)), {
    get(t, n) {
      if (n in t)
        return t[n];
      if (n in Dn)
        return Dn[n](e);
    },
    has(t, n) {
      return n in t || n in Dn;
    }
  })) : e.proxy;
}
const wg = /(?:^|[-_])(\w)/g, Eg = (e) => e.replace(wg, (t) => t.toUpperCase()).replace(/[-_]/g, "");
function _u(e, t = !0) {
  return K(e) ? e.displayName || e.name : e.name || t && e.__name;
}
function _o(e, t, n = !1) {
  let s = _u(t);
  if (!s && t.__file) {
    const i = t.__file.match(/([^/\\]+)\.\w+$/);
    i && (s = i[1]);
  }
  if (!s && e && e.parent) {
    const i = (o) => {
      for (const r in o)
        if (o[r] === t)
          return r;
    };
    s = i(
      e.components || e.parent.type.components
    ) || i(e.appContext.components);
  }
  return s ? Eg(s) : n ? "App" : "Anonymous";
}
function yu(e) {
  return K(e) && "__vccOpts" in e;
}
const Og = (e, t) => {
  const n = Td(e, t, $s);
  if (x.NODE_ENV !== "production") {
    const s = gg();
    s && s.appContext.config.warnRecursiveComputed && (n._warnRecursive = !0);
  }
  return n;
};
function Sg() {
  if (x.NODE_ENV === "production" || typeof window > "u")
    return;
  const e = { style: "color:#3ba776" }, t = { style: "color:#1677ff" }, n = { style: "color:#f5222d" }, s = { style: "color:#eb2f96" }, i = {
    __vue_custom_formatter: !0,
    header(u) {
      return dt(u) ? u.__isVue ? ["div", e, "VueInstance"] : kt(u) ? [
        "div",
        {},
        ["span", e, f(u)],
        "<",
        // avoid debugger accessing value affecting behavior
        a("_value" in u ? u._value : u),
        ">"
      ] : Mn(u) ? [
        "div",
        {},
        ["span", e, qt(u) ? "ShallowReactive" : "Reactive"],
        "<",
        a(u),
        `>${sn(u) ? " (readonly)" : ""}`
      ] : sn(u) ? [
        "div",
        {},
        ["span", e, qt(u) ? "ShallowReadonly" : "Readonly"],
        "<",
        a(u),
        ">"
      ] : null : null;
    },
    hasBody(u) {
      return u && u.__isVue;
    },
    body(u) {
      if (u && u.__isVue)
        return [
          "div",
          {},
          ...o(u.$)
        ];
    }
  };
  function o(u) {
    const h = [];
    u.type.props && u.props && h.push(r("props", et(u.props))), u.setupState !== ut && h.push(r("setup", u.setupState)), u.data !== ut && h.push(r("data", et(u.data)));
    const d = l(u, "computed");
    d && h.push(r("computed", d));
    const p = l(u, "inject");
    return p && h.push(r("injected", p)), h.push([
      "div",
      {},
      [
        "span",
        {
          style: s.style + ";opacity:0.66"
        },
        "$ (internal): "
      ],
      ["object", { object: u }]
    ]), h;
  }
  function r(u, h) {
    return h = _t({}, h), Object.keys(h).length ? [
      "div",
      { style: "line-height:1.25em;margin-bottom:0.6em" },
      [
        "div",
        {
          style: "color:#476582"
        },
        u
      ],
      [
        "div",
        {
          style: "padding-left:1.25em"
        },
        ...Object.keys(h).map((d) => [
          "div",
          {},
          ["span", s, d + ": "],
          a(h[d], !1)
        ])
      ]
    ] : ["span", {}];
  }
  function a(u, h = !0) {
    return typeof u == "number" ? ["span", t, u] : typeof u == "string" ? ["span", n, JSON.stringify(u)] : typeof u == "boolean" ? ["span", s, u] : dt(u) ? ["object", { object: h ? et(u) : u }] : ["span", n, String(u)];
  }
  function l(u, h) {
    const d = u.type;
    if (K(d))
      return;
    const p = {};
    for (const g in u.ctx)
      c(d, g, h) && (p[g] = u.ctx[g]);
    return p;
  }
  function c(u, h, d) {
    const p = u[d];
    if (U(p) && p.includes(h) || dt(p) && h in p || u.extends && c(u.extends, h, d) || u.mixins && u.mixins.some((g) => c(g, h, d)))
      return !0;
  }
  function f(u) {
    return qt(u) ? "ShallowRef" : u.effect ? "ComputedRef" : "Ref";
  }
  window.devtoolsFormatters ? window.devtoolsFormatters.push(i) : window.devtoolsFormatters = [i];
}
const rl = "3.5.13", se = x.NODE_ENV !== "production" ? R : St;
var Tt = {};
let Er;
const al = typeof window < "u" && window.trustedTypes;
if (al)
  try {
    Er = /* @__PURE__ */ al.createPolicy("vue", {
      createHTML: (e) => e
    });
  } catch (e) {
    Tt.NODE_ENV !== "production" && se(`Error creating trusted types policy: ${e}`);
  }
const xu = Er ? (e) => Er.createHTML(e) : (e) => e, Mg = "http://www.w3.org/2000/svg", kg = "http://www.w3.org/1998/Math/MathML", je = typeof document < "u" ? document : null, ll = je && /* @__PURE__ */ je.createElement("template"), Ng = {
  insert: (e, t, n) => {
    t.insertBefore(e, n || null);
  },
  remove: (e) => {
    const t = e.parentNode;
    t && t.removeChild(e);
  },
  createElement: (e, t, n, s) => {
    const i = t === "svg" ? je.createElementNS(Mg, e) : t === "mathml" ? je.createElementNS(kg, e) : n ? je.createElement(e, { is: n }) : je.createElement(e);
    return e === "select" && s && s.multiple != null && i.setAttribute("multiple", s.multiple), i;
  },
  createText: (e) => je.createTextNode(e),
  createComment: (e) => je.createComment(e),
  setText: (e, t) => {
    e.nodeValue = t;
  },
  setElementText: (e, t) => {
    e.textContent = t;
  },
  parentNode: (e) => e.parentNode,
  nextSibling: (e) => e.nextSibling,
  querySelector: (e) => je.querySelector(e),
  setScopeId(e, t) {
    e.setAttribute(t, "");
  },
  // __UNSAFE__
  // Reason: innerHTML.
  // Static content here can only come from compiled templates.
  // As long as the user only uses trusted templates, this is safe.
  insertStaticContent(e, t, n, s, i, o) {
    const r = n ? n.previousSibling : t.lastChild;
    if (i && (i === o || i.nextSibling))
      for (; t.insertBefore(i.cloneNode(!0), n), !(i === o || !(i = i.nextSibling)); )
        ;
    else {
      ll.innerHTML = xu(
        s === "svg" ? `<svg>${e}</svg>` : s === "mathml" ? `<math>${e}</math>` : e
      );
      const a = ll.content;
      if (s === "svg" || s === "mathml") {
        const l = a.firstChild;
        for (; l.firstChild; )
          a.appendChild(l.firstChild);
        a.removeChild(l);
      }
      t.insertBefore(a, n);
    }
    return [
      // first
      r ? r.nextSibling : t.firstChild,
      // last
      n ? n.previousSibling : t.lastChild
    ];
  }
}, Dg = Symbol("_vtc");
function Cg(e, t, n) {
  const s = e[Dg];
  s && (t = (t ? [t, ...s] : [...s]).join(" ")), t == null ? e.removeAttribute("class") : n ? e.setAttribute("class", t) : e.className = t;
}
const cl = Symbol("_vod"), Pg = Symbol("_vsh"), Tg = Symbol(Tt.NODE_ENV !== "production" ? "CSS_VAR_TEXT" : ""), Ag = /(^|;)\s*display\s*:/;
function Vg(e, t, n) {
  const s = e.style, i = bt(n);
  let o = !1;
  if (n && !i) {
    if (t)
      if (bt(t))
        for (const r of t.split(";")) {
          const a = r.slice(0, r.indexOf(":")).trim();
          n[a] == null && Ci(s, a, "");
        }
      else
        for (const r in t)
          n[r] == null && Ci(s, r, "");
    for (const r in n)
      r === "display" && (o = !0), Ci(s, r, n[r]);
  } else if (i) {
    if (t !== n) {
      const r = s[Tg];
      r && (n += ";" + r), s.cssText = n, o = Ag.test(n);
    }
  } else t && e.removeAttribute("style");
  cl in e && (e[cl] = o ? s.display : "", e[Pg] && (s.display = "none"));
}
const Rg = /[^\\];\s*$/, fl = /\s*!important$/;
function Ci(e, t, n) {
  if (U(n))
    n.forEach((s) => Ci(e, t, s));
  else if (n == null && (n = ""), Tt.NODE_ENV !== "production" && Rg.test(n) && se(
    `Unexpected semicolon at the end of '${t}' style value: '${n}'`
  ), t.startsWith("--"))
    e.setProperty(t, n);
  else {
    const s = Ig(e, t);
    fl.test(n) ? e.setProperty(
      Zt(s),
      n.replace(fl, ""),
      "important"
    ) : e[s] = n;
  }
}
const ul = ["Webkit", "Moz", "ms"], Ro = {};
function Ig(e, t) {
  const n = Ro[t];
  if (n)
    return n;
  let s = Kt(t);
  if (s !== "filter" && s in e)
    return Ro[t] = s;
  s = lo(s);
  for (let i = 0; i < ul.length; i++) {
    const o = ul[i] + s;
    if (o in e)
      return Ro[t] = o;
  }
  return t;
}
const hl = "http://www.w3.org/1999/xlink";
function dl(e, t, n, s, i, o = ad(t)) {
  s && t.startsWith("xlink:") ? n == null ? e.removeAttributeNS(hl, t.slice(6, t.length)) : e.setAttributeNS(hl, t, n) : n == null || o && !sf(n) ? e.removeAttribute(t) : e.setAttribute(
    t,
    o ? "" : ln(n) ? String(n) : n
  );
}
function pl(e, t, n, s, i) {
  if (t === "innerHTML" || t === "textContent") {
    n != null && (e[t] = t === "innerHTML" ? xu(n) : n);
    return;
  }
  const o = e.tagName;
  if (t === "value" && o !== "PROGRESS" && // custom elements may use _value internally
  !o.includes("-")) {
    const a = o === "OPTION" ? e.getAttribute("value") || "" : e.value, l = n == null ? (
      // #11647: value should be set as empty string for null and undefined,
      // but <input type="checkbox"> should be set as 'on'.
      e.type === "checkbox" ? "on" : ""
    ) : String(n);
    (a !== l || !("_value" in e)) && (e.value = l), n == null && e.removeAttribute(t), e._value = n;
    return;
  }
  let r = !1;
  if (n === "" || n == null) {
    const a = typeof e[t];
    a === "boolean" ? n = sf(n) : n == null && a === "string" ? (n = "", r = !0) : a === "number" && (n = 0, r = !0);
  }
  try {
    e[t] = n;
  } catch (a) {
    Tt.NODE_ENV !== "production" && !r && se(
      `Failed setting prop "${t}" on <${o.toLowerCase()}>: value ${n} is invalid.`,
      a
    );
  }
  r && e.removeAttribute(i || t);
}
function Lg(e, t, n, s) {
  e.addEventListener(t, n, s);
}
function Fg(e, t, n, s) {
  e.removeEventListener(t, n, s);
}
const gl = Symbol("_vei");
function $g(e, t, n, s, i = null) {
  const o = e[gl] || (e[gl] = {}), r = o[t];
  if (s && r)
    r.value = Tt.NODE_ENV !== "production" ? bl(s, t) : s;
  else {
    const [a, l] = Bg(t);
    if (s) {
      const c = o[t] = Hg(
        Tt.NODE_ENV !== "production" ? bl(s, t) : s,
        i
      );
      Lg(e, a, c, l);
    } else r && (Fg(e, a, r, l), o[t] = void 0);
  }
}
const ml = /(?:Once|Passive|Capture)$/;
function Bg(e) {
  let t;
  if (ml.test(e)) {
    t = {};
    let s;
    for (; s = e.match(ml); )
      e = e.slice(0, e.length - s[0].length), t[s[0].toLowerCase()] = !0;
  }
  return [e[2] === ":" ? e.slice(3) : Zt(e.slice(2)), t];
}
let Io = 0;
const jg = /* @__PURE__ */ Promise.resolve(), zg = () => Io || (jg.then(() => Io = 0), Io = Date.now());
function Hg(e, t) {
  const n = (s) => {
    if (!s._vts)
      s._vts = Date.now();
    else if (s._vts <= n.attached)
      return;
    Ve(
      Wg(s, n.value),
      t,
      5,
      [s]
    );
  };
  return n.value = e, n.attached = zg(), n;
}
function bl(e, t) {
  return K(e) || U(e) ? e : (se(
    `Wrong type passed as event handler to ${t} - did you forget @ or : in front of your prop?
Expected function or array of functions, received type ${typeof e}.`
  ), St);
}
function Wg(e, t) {
  if (U(t)) {
    const n = e.stopImmediatePropagation;
    return e.stopImmediatePropagation = () => {
      n.call(e), e._stopped = !0;
    }, t.map(
      (s) => (i) => !i._stopped && s && s(i)
    );
  } else
    return t;
}
const _l = (e) => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && // lowercase letter
e.charCodeAt(2) > 96 && e.charCodeAt(2) < 123, Ug = (e, t, n, s, i, o) => {
  const r = i === "svg";
  t === "class" ? Cg(e, s, r) : t === "style" ? Vg(e, n, s) : Us(t) ? Ii(t) || $g(e, t, n, s, o) : (t[0] === "." ? (t = t.slice(1), !0) : t[0] === "^" ? (t = t.slice(1), !1) : Yg(e, t, s, r)) ? (pl(e, t, s), !e.tagName.includes("-") && (t === "value" || t === "checked" || t === "selected") && dl(e, t, s, r, o, t !== "value")) : /* #11081 force set props for possible async custom element */ e._isVueCE && (/[A-Z]/.test(t) || !bt(s)) ? pl(e, Kt(t), s, o, t) : (t === "true-value" ? e._trueValue = s : t === "false-value" && (e._falseValue = s), dl(e, t, s, r));
};
function Yg(e, t, n, s) {
  if (s)
    return !!(t === "innerHTML" || t === "textContent" || t in e && _l(t) && K(n));
  if (t === "spellcheck" || t === "draggable" || t === "translate" || t === "form" || t === "list" && e.tagName === "INPUT" || t === "type" && e.tagName === "TEXTAREA")
    return !1;
  if (t === "width" || t === "height") {
    const i = e.tagName;
    if (i === "IMG" || i === "VIDEO" || i === "CANVAS" || i === "SOURCE")
      return !1;
  }
  return _l(t) && bt(n) ? !1 : t in e;
}
const yl = {};
/*! #__NO_SIDE_EFFECTS__ */
// @__NO_SIDE_EFFECTS__
function Kg(e, t, n) {
  const s = /* @__PURE__ */ ip(e, t);
  ro(s) && _t(s, t);
  class i extends aa {
    constructor(r) {
      super(s, r, n);
    }
  }
  return i.def = s, i;
}
const qg = typeof HTMLElement < "u" ? HTMLElement : class {
};
class aa extends qg {
  constructor(t, n = {}, s = vl) {
    super(), this._def = t, this._props = n, this._createApp = s, this._isVueCE = !0, this._instance = null, this._app = null, this._nonce = this._def.nonce, this._connected = !1, this._resolved = !1, this._numberProps = null, this._styleChildren = /* @__PURE__ */ new WeakSet(), this._ob = null, this.shadowRoot && s !== vl ? this._root = this.shadowRoot : (Tt.NODE_ENV !== "production" && this.shadowRoot && se(
      "Custom element has pre-rendered declarative shadow root but is not defined as hydratable. Use `defineSSRCustomElement`."
    ), t.shadowRoot !== !1 ? (this.attachShadow({ mode: "open" }), this._root = this.shadowRoot) : this._root = this), this._def.__asyncLoader || this._resolveProps(this._def);
  }
  connectedCallback() {
    if (!this.isConnected) return;
    this.shadowRoot || this._parseSlots(), this._connected = !0;
    let t = this;
    for (; t = t && (t.parentNode || t.host); )
      if (t instanceof aa) {
        this._parent = t;
        break;
      }
    this._instance || (this._resolved ? (this._setParent(), this._update()) : t && t._pendingResolve ? this._pendingResolve = t._pendingResolve.then(() => {
      this._pendingResolve = void 0, this._resolveDef();
    }) : this._resolveDef());
  }
  _setParent(t = this._parent) {
    t && (this._instance.parent = t._instance, this._instance.provides = t._instance.provides);
  }
  disconnectedCallback() {
    this._connected = !1, Df(() => {
      this._connected || (this._ob && (this._ob.disconnect(), this._ob = null), this._app && this._app.unmount(), this._instance && (this._instance.ce = void 0), this._app = this._instance = null);
    });
  }
  /**
   * resolve inner component definition (handle possible async component)
   */
  _resolveDef() {
    if (this._pendingResolve)
      return;
    for (let s = 0; s < this.attributes.length; s++)
      this._setAttr(this.attributes[s].name);
    this._ob = new MutationObserver((s) => {
      for (const i of s)
        this._setAttr(i.attributeName);
    }), this._ob.observe(this, { attributes: !0 });
    const t = (s, i = !1) => {
      this._resolved = !0, this._pendingResolve = void 0;
      const { props: o, styles: r } = s;
      let a;
      if (o && !U(o))
        for (const l in o) {
          const c = o[l];
          (c === Number || c && c.type === Number) && (l in this._props && (this._props[l] = Ra(this._props[l])), (a || (a = /* @__PURE__ */ Object.create(null)))[Kt(l)] = !0);
        }
      this._numberProps = a, i && this._resolveProps(s), this.shadowRoot ? this._applyStyles(r) : Tt.NODE_ENV !== "production" && r && se(
        "Custom element style injection is not supported when using shadowRoot: false"
      ), this._mount(s);
    }, n = this._def.__asyncLoader;
    n ? this._pendingResolve = n().then(
      (s) => t(this._def = s, !0)
    ) : t(this._def);
  }
  _mount(t) {
    Tt.NODE_ENV !== "production" && !t.name && (t.name = "VueElement"), this._app = this._createApp(t), t.configureApp && t.configureApp(this._app), this._app._ceVNode = this._createVNode(), this._app.mount(this._root);
    const n = this._instance && this._instance.exposed;
    if (n)
      for (const s in n)
        at(this, s) ? Tt.NODE_ENV !== "production" && se(`Exposed property "${s}" already exists on custom element.`) : Object.defineProperty(this, s, {
          // unwrap ref to be consistent with public instance behavior
          get: () => Sf(n[s])
        });
  }
  _resolveProps(t) {
    const { props: n } = t, s = U(n) ? n : Object.keys(n || {});
    for (const i of Object.keys(this))
      i[0] !== "_" && s.includes(i) && this._setProp(i, this[i]);
    for (const i of s.map(Kt))
      Object.defineProperty(this, i, {
        get() {
          return this._getProp(i);
        },
        set(o) {
          this._setProp(i, o, !0, !0);
        }
      });
  }
  _setAttr(t) {
    if (t.startsWith("data-v-")) return;
    const n = this.hasAttribute(t);
    let s = n ? this.getAttribute(t) : yl;
    const i = Kt(t);
    n && this._numberProps && this._numberProps[i] && (s = Ra(s)), this._setProp(i, s, !1, !0);
  }
  /**
   * @internal
   */
  _getProp(t) {
    return this._props[t];
  }
  /**
   * @internal
   */
  _setProp(t, n, s = !0, i = !1) {
    if (n !== this._props[t] && (n === yl ? delete this._props[t] : (this._props[t] = n, t === "key" && this._app && (this._app._ceVNode.key = n)), i && this._instance && this._update(), s)) {
      const o = this._ob;
      o && o.disconnect(), n === !0 ? this.setAttribute(Zt(t), "") : typeof n == "string" || typeof n == "number" ? this.setAttribute(Zt(t), n + "") : n || this.removeAttribute(Zt(t)), o && o.observe(this, { attributes: !0 });
    }
  }
  _update() {
    Gg(this._createVNode(), this._root);
  }
  _createVNode() {
    const t = {};
    this.shadowRoot || (t.onVnodeMounted = t.onVnodeUpdated = this._renderSlots.bind(this));
    const n = De(this._def, _t(t, this._props));
    return this._instance || (n.ce = (s) => {
      this._instance = s, s.ce = this, s.isCE = !0, Tt.NODE_ENV !== "production" && (s.ceReload = (o) => {
        this._styles && (this._styles.forEach((r) => this._root.removeChild(r)), this._styles.length = 0), this._applyStyles(o), this._instance = null, this._update();
      });
      const i = (o, r) => {
        this.dispatchEvent(
          new CustomEvent(
            o,
            ro(r[0]) ? _t({ detail: r }, r[0]) : { detail: r }
          )
        );
      };
      s.emit = (o, ...r) => {
        i(o, r), Zt(o) !== o && i(Zt(o), r);
      }, this._setParent();
    }), n;
  }
  _applyStyles(t, n) {
    if (!t) return;
    if (n) {
      if (n === this._def || this._styleChildren.has(n))
        return;
      this._styleChildren.add(n);
    }
    const s = this._nonce;
    for (let i = t.length - 1; i >= 0; i--) {
      const o = document.createElement("style");
      if (s && o.setAttribute("nonce", s), o.textContent = t[i], this.shadowRoot.prepend(o), Tt.NODE_ENV !== "production")
        if (n) {
          if (n.__hmrId) {
            this._childStyles || (this._childStyles = /* @__PURE__ */ new Map());
            let r = this._childStyles.get(n.__hmrId);
            r || this._childStyles.set(n.__hmrId, r = []), r.push(o);
          }
        } else
          (this._styles || (this._styles = [])).push(o);
    }
  }
  /**
   * Only called when shadowRoot is false
   */
  _parseSlots() {
    const t = this._slots = {};
    let n;
    for (; n = this.firstChild; ) {
      const s = n.nodeType === 1 && n.getAttribute("slot") || "default";
      (t[s] || (t[s] = [])).push(n), this.removeChild(n);
    }
  }
  /**
   * Only called when shadowRoot is false
   */
  _renderSlots() {
    const t = (this._teleportTarget || this).querySelectorAll("slot"), n = this._instance.type.__scopeId;
    for (let s = 0; s < t.length; s++) {
      const i = t[s], o = i.getAttribute("name") || "default", r = this._slots[o], a = i.parentNode;
      if (r)
        for (const l of r) {
          if (n && l.nodeType === 1) {
            const c = n + "-s", f = document.createTreeWalker(l, 1);
            l.setAttribute(c, "");
            let u;
            for (; u = f.nextNode(); )
              u.setAttribute(c, "");
          }
          a.insertBefore(l, i);
        }
      else
        for (; i.firstChild; ) a.insertBefore(i.firstChild, i);
      a.removeChild(i);
    }
  }
  /**
   * @internal
   */
  _injectChildStyle(t) {
    this._applyStyles(t.styles, t);
  }
  /**
   * @internal
   */
  _removeChildStyle(t) {
    if (Tt.NODE_ENV !== "production" && (this._styleChildren.delete(t), this._childStyles && t.__hmrId)) {
      const n = this._childStyles.get(t.__hmrId);
      n && (n.forEach((s) => this._root.removeChild(s)), n.length = 0);
    }
  }
}
const Xg = /* @__PURE__ */ _t({ patchProp: Ug }, Ng);
let xl;
function vu() {
  return xl || (xl = Yp(Xg));
}
const Gg = (...e) => {
  vu().render(...e);
}, vl = (...e) => {
  const t = vu().createApp(...e);
  Tt.NODE_ENV !== "production" && (Jg(t), Qg(t));
  const { mount: n } = t;
  return t.mount = (s) => {
    const i = tm(s);
    if (!i) return;
    const o = t._component;
    !K(o) && !o.render && !o.template && (o.template = i.innerHTML), i.nodeType === 1 && (i.textContent = "");
    const r = n(i, !1, Zg(i));
    return i instanceof Element && (i.removeAttribute("v-cloak"), i.setAttribute("data-v-app", "")), r;
  }, t;
};
function Zg(e) {
  if (e instanceof SVGElement)
    return "svg";
  if (typeof MathMLElement == "function" && e instanceof MathMLElement)
    return "mathml";
}
function Jg(e) {
  Object.defineProperty(e.config, "isNativeTag", {
    value: (t) => sd(t) || id(t) || od(t),
    writable: !1
  });
}
function Qg(e) {
  {
    const t = e.config.isCustomElement;
    Object.defineProperty(e.config, "isCustomElement", {
      get() {
        return t;
      },
      set() {
        se(
          "The `isCustomElement` config option is deprecated. Use `compilerOptions.isCustomElement` instead."
        );
      }
    });
    const n = e.config.compilerOptions, s = 'The `compilerOptions` config option is only respected when using a build of Vue.js that includes the runtime compiler (aka "full build"). Since you are using the runtime-only build, `compilerOptions` must be passed to `@vue/compiler-dom` in the build setup instead.\n- For vue-loader: pass it via vue-loader\'s `compilerOptions` loader option.\n- For vue-cli: see https://cli.vuejs.org/guide/webpack.html#modifying-options-of-a-loader\n- For vite: pass it via @vitejs/plugin-vue options. See https://github.com/vitejs/vite-plugin-vue/tree/main/packages/plugin-vue#example-for-passing-options-to-vuecompiler-sfc';
    Object.defineProperty(e.config, "compilerOptions", {
      get() {
        return se(s), n;
      },
      set() {
        se(s);
      }
    });
  }
}
function tm(e) {
  if (bt(e)) {
    const t = document.querySelector(e);
    return Tt.NODE_ENV !== "production" && !t && se(
      `Failed to mount app: mount target selector "${e}" returned null.`
    ), t;
  }
  return Tt.NODE_ENV !== "production" && window.ShadowRoot && e instanceof window.ShadowRoot && e.mode === "closed" && se(
    'mounting on a ShadowRoot with `{mode: "closed"}` may lead to unpredictable bugs'
  ), e;
}
var em = {};
function nm() {
  Sg();
}
em.NODE_ENV !== "production" && nm();
/*!
 * @kurkle/color v0.3.4
 * https://github.com/kurkle/color#readme
 * (c) 2024 Jukka Kurkela
 * Released under the MIT License
 */
function Zs(e) {
  return e + 0.5 | 0;
}
const tn = (e, t, n) => Math.max(Math.min(e, n), t);
function xs(e) {
  return tn(Zs(e * 2.55), 0, 255);
}
function nn(e) {
  return tn(Zs(e * 255), 0, 255);
}
function ze(e) {
  return tn(Zs(e / 2.55) / 100, 0, 1);
}
function wl(e) {
  return tn(Zs(e * 100), 0, 100);
}
const ne = { 0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, A: 10, B: 11, C: 12, D: 13, E: 14, F: 15, a: 10, b: 11, c: 12, d: 13, e: 14, f: 15 }, Or = [..."0123456789ABCDEF"], sm = (e) => Or[e & 15], im = (e) => Or[(e & 240) >> 4] + Or[e & 15], si = (e) => (e & 240) >> 4 === (e & 15), om = (e) => si(e.r) && si(e.g) && si(e.b) && si(e.a);
function rm(e) {
  var t = e.length, n;
  return e[0] === "#" && (t === 4 || t === 5 ? n = {
    r: 255 & ne[e[1]] * 17,
    g: 255 & ne[e[2]] * 17,
    b: 255 & ne[e[3]] * 17,
    a: t === 5 ? ne[e[4]] * 17 : 255
  } : (t === 7 || t === 9) && (n = {
    r: ne[e[1]] << 4 | ne[e[2]],
    g: ne[e[3]] << 4 | ne[e[4]],
    b: ne[e[5]] << 4 | ne[e[6]],
    a: t === 9 ? ne[e[7]] << 4 | ne[e[8]] : 255
  })), n;
}
const am = (e, t) => e < 255 ? t(e) : "";
function lm(e) {
  var t = om(e) ? sm : im;
  return e ? "#" + t(e.r) + t(e.g) + t(e.b) + am(e.a, t) : void 0;
}
const cm = /^(hsla?|hwb|hsv)\(\s*([-+.e\d]+)(?:deg)?[\s,]+([-+.e\d]+)%[\s,]+([-+.e\d]+)%(?:[\s,]+([-+.e\d]+)(%)?)?\s*\)$/;
function wu(e, t, n) {
  const s = t * Math.min(n, 1 - n), i = (o, r = (o + e / 30) % 12) => n - s * Math.max(Math.min(r - 3, 9 - r, 1), -1);
  return [i(0), i(8), i(4)];
}
function fm(e, t, n) {
  const s = (i, o = (i + e / 60) % 6) => n - n * t * Math.max(Math.min(o, 4 - o, 1), 0);
  return [s(5), s(3), s(1)];
}
function um(e, t, n) {
  const s = wu(e, 1, 0.5);
  let i;
  for (t + n > 1 && (i = 1 / (t + n), t *= i, n *= i), i = 0; i < 3; i++)
    s[i] *= 1 - t - n, s[i] += t;
  return s;
}
function hm(e, t, n, s, i) {
  return e === i ? (t - n) / s + (t < n ? 6 : 0) : t === i ? (n - e) / s + 2 : (e - t) / s + 4;
}
function la(e) {
  const n = e.r / 255, s = e.g / 255, i = e.b / 255, o = Math.max(n, s, i), r = Math.min(n, s, i), a = (o + r) / 2;
  let l, c, f;
  return o !== r && (f = o - r, c = a > 0.5 ? f / (2 - o - r) : f / (o + r), l = hm(n, s, i, f, o), l = l * 60 + 0.5), [l | 0, c || 0, a];
}
function ca(e, t, n, s) {
  return (Array.isArray(t) ? e(t[0], t[1], t[2]) : e(t, n, s)).map(nn);
}
function fa(e, t, n) {
  return ca(wu, e, t, n);
}
function dm(e, t, n) {
  return ca(um, e, t, n);
}
function pm(e, t, n) {
  return ca(fm, e, t, n);
}
function Eu(e) {
  return (e % 360 + 360) % 360;
}
function gm(e) {
  const t = cm.exec(e);
  let n = 255, s;
  if (!t)
    return;
  t[5] !== s && (n = t[6] ? xs(+t[5]) : nn(+t[5]));
  const i = Eu(+t[2]), o = +t[3] / 100, r = +t[4] / 100;
  return t[1] === "hwb" ? s = dm(i, o, r) : t[1] === "hsv" ? s = pm(i, o, r) : s = fa(i, o, r), {
    r: s[0],
    g: s[1],
    b: s[2],
    a: n
  };
}
function mm(e, t) {
  var n = la(e);
  n[0] = Eu(n[0] + t), n = fa(n), e.r = n[0], e.g = n[1], e.b = n[2];
}
function bm(e) {
  if (!e)
    return;
  const t = la(e), n = t[0], s = wl(t[1]), i = wl(t[2]);
  return e.a < 255 ? `hsla(${n}, ${s}%, ${i}%, ${ze(e.a)})` : `hsl(${n}, ${s}%, ${i}%)`;
}
const El = {
  x: "dark",
  Z: "light",
  Y: "re",
  X: "blu",
  W: "gr",
  V: "medium",
  U: "slate",
  A: "ee",
  T: "ol",
  S: "or",
  B: "ra",
  C: "lateg",
  D: "ights",
  R: "in",
  Q: "turquois",
  E: "hi",
  P: "ro",
  O: "al",
  N: "le",
  M: "de",
  L: "yello",
  F: "en",
  K: "ch",
  G: "arks",
  H: "ea",
  I: "ightg",
  J: "wh"
}, Ol = {
  OiceXe: "f0f8ff",
  antiquewEte: "faebd7",
  aqua: "ffff",
  aquamarRe: "7fffd4",
  azuY: "f0ffff",
  beige: "f5f5dc",
  bisque: "ffe4c4",
  black: "0",
  blanKedOmond: "ffebcd",
  Xe: "ff",
  XeviTet: "8a2be2",
  bPwn: "a52a2a",
  burlywood: "deb887",
  caMtXe: "5f9ea0",
  KartYuse: "7fff00",
  KocTate: "d2691e",
  cSO: "ff7f50",
  cSnflowerXe: "6495ed",
  cSnsilk: "fff8dc",
  crimson: "dc143c",
  cyan: "ffff",
  xXe: "8b",
  xcyan: "8b8b",
  xgTMnPd: "b8860b",
  xWay: "a9a9a9",
  xgYF: "6400",
  xgYy: "a9a9a9",
  xkhaki: "bdb76b",
  xmagFta: "8b008b",
  xTivegYF: "556b2f",
  xSange: "ff8c00",
  xScEd: "9932cc",
  xYd: "8b0000",
  xsOmon: "e9967a",
  xsHgYF: "8fbc8f",
  xUXe: "483d8b",
  xUWay: "2f4f4f",
  xUgYy: "2f4f4f",
  xQe: "ced1",
  xviTet: "9400d3",
  dAppRk: "ff1493",
  dApskyXe: "bfff",
  dimWay: "696969",
  dimgYy: "696969",
  dodgerXe: "1e90ff",
  fiYbrick: "b22222",
  flSOwEte: "fffaf0",
  foYstWAn: "228b22",
  fuKsia: "ff00ff",
  gaRsbSo: "dcdcdc",
  ghostwEte: "f8f8ff",
  gTd: "ffd700",
  gTMnPd: "daa520",
  Way: "808080",
  gYF: "8000",
  gYFLw: "adff2f",
  gYy: "808080",
  honeyMw: "f0fff0",
  hotpRk: "ff69b4",
  RdianYd: "cd5c5c",
  Rdigo: "4b0082",
  ivSy: "fffff0",
  khaki: "f0e68c",
  lavFMr: "e6e6fa",
  lavFMrXsh: "fff0f5",
  lawngYF: "7cfc00",
  NmoncEffon: "fffacd",
  ZXe: "add8e6",
  ZcSO: "f08080",
  Zcyan: "e0ffff",
  ZgTMnPdLw: "fafad2",
  ZWay: "d3d3d3",
  ZgYF: "90ee90",
  ZgYy: "d3d3d3",
  ZpRk: "ffb6c1",
  ZsOmon: "ffa07a",
  ZsHgYF: "20b2aa",
  ZskyXe: "87cefa",
  ZUWay: "778899",
  ZUgYy: "778899",
  ZstAlXe: "b0c4de",
  ZLw: "ffffe0",
  lime: "ff00",
  limegYF: "32cd32",
  lRF: "faf0e6",
  magFta: "ff00ff",
  maPon: "800000",
  VaquamarRe: "66cdaa",
  VXe: "cd",
  VScEd: "ba55d3",
  VpurpN: "9370db",
  VsHgYF: "3cb371",
  VUXe: "7b68ee",
  VsprRggYF: "fa9a",
  VQe: "48d1cc",
  VviTetYd: "c71585",
  midnightXe: "191970",
  mRtcYam: "f5fffa",
  mistyPse: "ffe4e1",
  moccasR: "ffe4b5",
  navajowEte: "ffdead",
  navy: "80",
  Tdlace: "fdf5e6",
  Tive: "808000",
  TivedBb: "6b8e23",
  Sange: "ffa500",
  SangeYd: "ff4500",
  ScEd: "da70d6",
  pOegTMnPd: "eee8aa",
  pOegYF: "98fb98",
  pOeQe: "afeeee",
  pOeviTetYd: "db7093",
  papayawEp: "ffefd5",
  pHKpuff: "ffdab9",
  peru: "cd853f",
  pRk: "ffc0cb",
  plum: "dda0dd",
  powMrXe: "b0e0e6",
  purpN: "800080",
  YbeccapurpN: "663399",
  Yd: "ff0000",
  Psybrown: "bc8f8f",
  PyOXe: "4169e1",
  saddNbPwn: "8b4513",
  sOmon: "fa8072",
  sandybPwn: "f4a460",
  sHgYF: "2e8b57",
  sHshell: "fff5ee",
  siFna: "a0522d",
  silver: "c0c0c0",
  skyXe: "87ceeb",
  UXe: "6a5acd",
  UWay: "708090",
  UgYy: "708090",
  snow: "fffafa",
  sprRggYF: "ff7f",
  stAlXe: "4682b4",
  tan: "d2b48c",
  teO: "8080",
  tEstN: "d8bfd8",
  tomato: "ff6347",
  Qe: "40e0d0",
  viTet: "ee82ee",
  JHt: "f5deb3",
  wEte: "ffffff",
  wEtesmoke: "f5f5f5",
  Lw: "ffff00",
  LwgYF: "9acd32"
};
function _m() {
  const e = {}, t = Object.keys(Ol), n = Object.keys(El);
  let s, i, o, r, a;
  for (s = 0; s < t.length; s++) {
    for (r = a = t[s], i = 0; i < n.length; i++)
      o = n[i], a = a.replace(o, El[o]);
    o = parseInt(Ol[r], 16), e[a] = [o >> 16 & 255, o >> 8 & 255, o & 255];
  }
  return e;
}
let ii;
function ym(e) {
  ii || (ii = _m(), ii.transparent = [0, 0, 0, 0]);
  const t = ii[e.toLowerCase()];
  return t && {
    r: t[0],
    g: t[1],
    b: t[2],
    a: t.length === 4 ? t[3] : 255
  };
}
const xm = /^rgba?\(\s*([-+.\d]+)(%)?[\s,]+([-+.e\d]+)(%)?[\s,]+([-+.e\d]+)(%)?(?:[\s,/]+([-+.e\d]+)(%)?)?\s*\)$/;
function vm(e) {
  const t = xm.exec(e);
  let n = 255, s, i, o;
  if (t) {
    if (t[7] !== s) {
      const r = +t[7];
      n = t[8] ? xs(r) : tn(r * 255, 0, 255);
    }
    return s = +t[1], i = +t[3], o = +t[5], s = 255 & (t[2] ? xs(s) : tn(s, 0, 255)), i = 255 & (t[4] ? xs(i) : tn(i, 0, 255)), o = 255 & (t[6] ? xs(o) : tn(o, 0, 255)), {
      r: s,
      g: i,
      b: o,
      a: n
    };
  }
}
function wm(e) {
  return e && (e.a < 255 ? `rgba(${e.r}, ${e.g}, ${e.b}, ${ze(e.a)})` : `rgb(${e.r}, ${e.g}, ${e.b})`);
}
const Lo = (e) => e <= 31308e-7 ? e * 12.92 : Math.pow(e, 1 / 2.4) * 1.055 - 0.055, $n = (e) => e <= 0.04045 ? e / 12.92 : Math.pow((e + 0.055) / 1.055, 2.4);
function Em(e, t, n) {
  const s = $n(ze(e.r)), i = $n(ze(e.g)), o = $n(ze(e.b));
  return {
    r: nn(Lo(s + n * ($n(ze(t.r)) - s))),
    g: nn(Lo(i + n * ($n(ze(t.g)) - i))),
    b: nn(Lo(o + n * ($n(ze(t.b)) - o))),
    a: e.a + n * (t.a - e.a)
  };
}
function oi(e, t, n) {
  if (e) {
    let s = la(e);
    s[t] = Math.max(0, Math.min(s[t] + s[t] * n, t === 0 ? 360 : 1)), s = fa(s), e.r = s[0], e.g = s[1], e.b = s[2];
  }
}
function Ou(e, t) {
  return e && Object.assign(t || {}, e);
}
function Sl(e) {
  var t = { r: 0, g: 0, b: 0, a: 255 };
  return Array.isArray(e) ? e.length >= 3 && (t = { r: e[0], g: e[1], b: e[2], a: 255 }, e.length > 3 && (t.a = nn(e[3]))) : (t = Ou(e, { r: 0, g: 0, b: 0, a: 1 }), t.a = nn(t.a)), t;
}
function Om(e) {
  return e.charAt(0) === "r" ? vm(e) : gm(e);
}
let Su = class Sr {
  constructor(t) {
    if (t instanceof Sr)
      return t;
    const n = typeof t;
    let s;
    n === "object" ? s = Sl(t) : n === "string" && (s = rm(t) || ym(t) || Om(t)), this._rgb = s, this._valid = !!s;
  }
  get valid() {
    return this._valid;
  }
  get rgb() {
    var t = Ou(this._rgb);
    return t && (t.a = ze(t.a)), t;
  }
  set rgb(t) {
    this._rgb = Sl(t);
  }
  rgbString() {
    return this._valid ? wm(this._rgb) : void 0;
  }
  hexString() {
    return this._valid ? lm(this._rgb) : void 0;
  }
  hslString() {
    return this._valid ? bm(this._rgb) : void 0;
  }
  mix(t, n) {
    if (t) {
      const s = this.rgb, i = t.rgb;
      let o;
      const r = n === o ? 0.5 : n, a = 2 * r - 1, l = s.a - i.a, c = ((a * l === -1 ? a : (a + l) / (1 + a * l)) + 1) / 2;
      o = 1 - c, s.r = 255 & c * s.r + o * i.r + 0.5, s.g = 255 & c * s.g + o * i.g + 0.5, s.b = 255 & c * s.b + o * i.b + 0.5, s.a = r * s.a + (1 - r) * i.a, this.rgb = s;
    }
    return this;
  }
  interpolate(t, n) {
    return t && (this._rgb = Em(this._rgb, t._rgb, n)), this;
  }
  clone() {
    return new Sr(this.rgb);
  }
  alpha(t) {
    return this._rgb.a = nn(t), this;
  }
  clearer(t) {
    const n = this._rgb;
    return n.a *= 1 - t, this;
  }
  greyscale() {
    const t = this._rgb, n = Zs(t.r * 0.3 + t.g * 0.59 + t.b * 0.11);
    return t.r = t.g = t.b = n, this;
  }
  opaquer(t) {
    const n = this._rgb;
    return n.a *= 1 + t, this;
  }
  negate() {
    const t = this._rgb;
    return t.r = 255 - t.r, t.g = 255 - t.g, t.b = 255 - t.b, this;
  }
  lighten(t) {
    return oi(this._rgb, 2, t), this;
  }
  darken(t) {
    return oi(this._rgb, 2, -t), this;
  }
  saturate(t) {
    return oi(this._rgb, 1, t), this;
  }
  desaturate(t) {
    return oi(this._rgb, 1, -t), this;
  }
  rotate(t) {
    return mm(this._rgb, t), this;
  }
};
/*!
 * Chart.js v4.4.7
 * https://www.chartjs.org
 * (c) 2024 Chart.js Contributors
 * Released under the MIT License
 */
function Le() {
}
const Sm = /* @__PURE__ */ (() => {
  let e = 0;
  return () => e++;
})();
function gt(e) {
  return e == null;
}
function Mt(e) {
  if (Array.isArray && Array.isArray(e))
    return !0;
  const t = Object.prototype.toString.call(e);
  return t.slice(0, 7) === "[object" && t.slice(-6) === "Array]";
}
function ot(e) {
  return e !== null && Object.prototype.toString.call(e) === "[object Object]";
}
function Rt(e) {
  return (typeof e == "number" || e instanceof Number) && isFinite(+e);
}
function xe(e, t) {
  return Rt(e) ? e : t;
}
function ht(e, t) {
  return typeof e > "u" ? t : e;
}
const Mm = (e, t) => typeof e == "string" && e.endsWith("%") ? parseFloat(e) / 100 * t : +e;
function yt(e, t, n) {
  if (e && typeof e.call == "function")
    return e.apply(n, t);
}
function ft(e, t, n, s) {
  let i, o, r;
  if (Mt(e))
    for (o = e.length, i = 0; i < o; i++)
      t.call(n, e[i], i);
  else if (ot(e))
    for (r = Object.keys(e), o = r.length, i = 0; i < o; i++)
      t.call(n, e[r[i]], r[i]);
}
function qi(e, t) {
  let n, s, i, o;
  if (!e || !t || e.length !== t.length)
    return !1;
  for (n = 0, s = e.length; n < s; ++n)
    if (i = e[n], o = t[n], i.datasetIndex !== o.datasetIndex || i.index !== o.index)
      return !1;
  return !0;
}
function Xi(e) {
  if (Mt(e))
    return e.map(Xi);
  if (ot(e)) {
    const t = /* @__PURE__ */ Object.create(null), n = Object.keys(e), s = n.length;
    let i = 0;
    for (; i < s; ++i)
      t[n[i]] = Xi(e[n[i]]);
    return t;
  }
  return e;
}
function Mu(e) {
  return [
    "__proto__",
    "prototype",
    "constructor"
  ].indexOf(e) === -1;
}
function km(e, t, n, s) {
  if (!Mu(e))
    return;
  const i = t[e], o = n[e];
  ot(i) && ot(o) ? Bs(i, o, s) : t[e] = Xi(o);
}
function Bs(e, t, n) {
  const s = Mt(t) ? t : [
    t
  ], i = s.length;
  if (!ot(e))
    return e;
  n = n || {};
  const o = n.merger || km;
  let r;
  for (let a = 0; a < i; ++a) {
    if (r = s[a], !ot(r))
      continue;
    const l = Object.keys(r);
    for (let c = 0, f = l.length; c < f; ++c)
      o(l[c], e, r, n);
  }
  return e;
}
function Ds(e, t) {
  return Bs(e, t, {
    merger: Nm
  });
}
function Nm(e, t, n) {
  if (!Mu(e))
    return;
  const s = t[e], i = n[e];
  ot(s) && ot(i) ? Ds(s, i) : Object.prototype.hasOwnProperty.call(t, e) || (t[e] = Xi(i));
}
const Ml = {
  // Chart.helpers.core resolveObjectKey should resolve empty key to root object
  "": (e) => e,
  // default resolvers
  x: (e) => e.x,
  y: (e) => e.y
};
function Dm(e) {
  const t = e.split("."), n = [];
  let s = "";
  for (const i of t)
    s += i, s.endsWith("\\") ? s = s.slice(0, -1) + "." : (n.push(s), s = "");
  return n;
}
function Cm(e) {
  const t = Dm(e);
  return (n) => {
    for (const s of t) {
      if (s === "")
        break;
      n = n && n[s];
    }
    return n;
  };
}
function Kn(e, t) {
  return (Ml[t] || (Ml[t] = Cm(t)))(e);
}
function ua(e) {
  return e.charAt(0).toUpperCase() + e.slice(1);
}
const js = (e) => typeof e < "u", rn = (e) => typeof e == "function", kl = (e, t) => {
  if (e.size !== t.size)
    return !1;
  for (const n of e)
    if (!t.has(n))
      return !1;
  return !0;
};
function Pm(e) {
  return e.type === "mouseup" || e.type === "click" || e.type === "contextmenu";
}
const Vt = Math.PI, Ce = 2 * Vt, Tm = Ce + Vt, Gi = Number.POSITIVE_INFINITY, Am = Vt / 180, ue = Vt / 2, pn = Vt / 4, Nl = Vt * 2 / 3, ku = Math.log10, Pe = Math.sign;
function Cs(e, t, n) {
  return Math.abs(e - t) < n;
}
function Dl(e) {
  const t = Math.round(e);
  e = Cs(e, t, e / 1e3) ? t : e;
  const n = Math.pow(10, Math.floor(ku(e))), s = e / n;
  return (s <= 1 ? 1 : s <= 2 ? 2 : s <= 5 ? 5 : 10) * n;
}
function Vm(e) {
  const t = [], n = Math.sqrt(e);
  let s;
  for (s = 1; s < n; s++)
    e % s === 0 && (t.push(s), t.push(e / s));
  return n === (n | 0) && t.push(n), t.sort((i, o) => i - o).pop(), t;
}
function Zi(e) {
  return !isNaN(parseFloat(e)) && isFinite(e);
}
function Rm(e, t) {
  const n = Math.round(e);
  return n - t <= e && n + t >= e;
}
function Im(e, t, n) {
  let s, i, o;
  for (s = 0, i = e.length; s < i; s++)
    o = e[s][n], isNaN(o) || (t.min = Math.min(t.min, o), t.max = Math.max(t.max, o));
}
function vn(e) {
  return e * (Vt / 180);
}
function Lm(e) {
  return e * (180 / Vt);
}
function Cl(e) {
  if (!Rt(e))
    return;
  let t = 1, n = 0;
  for (; Math.round(e * t) / t !== e; )
    t *= 10, n++;
  return n;
}
function Fm(e, t) {
  const n = t.x - e.x, s = t.y - e.y, i = Math.sqrt(n * n + s * s);
  let o = Math.atan2(s, n);
  return o < -0.5 * Vt && (o += Ce), {
    angle: o,
    distance: i
  };
}
function Mr(e, t) {
  return Math.sqrt(Math.pow(t.x - e.x, 2) + Math.pow(t.y - e.y, 2));
}
function $m(e, t) {
  return (e - t + Tm) % Ce - Vt;
}
function Oe(e) {
  return (e % Ce + Ce) % Ce;
}
function Nu(e, t, n, s) {
  const i = Oe(e), o = Oe(t), r = Oe(n), a = Oe(o - i), l = Oe(r - i), c = Oe(i - o), f = Oe(i - r);
  return i === o || i === r || s && o === r || a > l && c < f;
}
function he(e, t, n) {
  return Math.max(t, Math.min(n, e));
}
function Bm(e) {
  return he(e, -32768, 32767);
}
function Ji(e, t, n, s = 1e-6) {
  return e >= Math.min(t, n) - s && e <= Math.max(t, n) + s;
}
function ha(e, t, n) {
  n = n || ((r) => e[r] < t);
  let s = e.length - 1, i = 0, o;
  for (; s - i > 1; )
    o = i + s >> 1, n(o) ? i = o : s = o;
  return {
    lo: i,
    hi: s
  };
}
const kr = (e, t, n, s) => ha(e, n, s ? (i) => {
  const o = e[i][t];
  return o < n || o === n && e[i + 1][t] === n;
} : (i) => e[i][t] < n), jm = (e, t, n) => ha(e, n, (s) => e[s][t] >= n);
function zm(e, t, n) {
  let s = 0, i = e.length;
  for (; s < i && e[s] < t; )
    s++;
  for (; i > s && e[i - 1] > n; )
    i--;
  return s > 0 || i < e.length ? e.slice(s, i) : e;
}
const Du = [
  "push",
  "pop",
  "shift",
  "splice",
  "unshift"
];
function Hm(e, t) {
  if (e._chartjs) {
    e._chartjs.listeners.push(t);
    return;
  }
  Object.defineProperty(e, "_chartjs", {
    configurable: !0,
    enumerable: !1,
    value: {
      listeners: [
        t
      ]
    }
  }), Du.forEach((n) => {
    const s = "_onData" + ua(n), i = e[n];
    Object.defineProperty(e, n, {
      configurable: !0,
      enumerable: !1,
      value(...o) {
        const r = i.apply(this, o);
        return e._chartjs.listeners.forEach((a) => {
          typeof a[s] == "function" && a[s](...o);
        }), r;
      }
    });
  });
}
function Pl(e, t) {
  const n = e._chartjs;
  if (!n)
    return;
  const s = n.listeners, i = s.indexOf(t);
  i !== -1 && s.splice(i, 1), !(s.length > 0) && (Du.forEach((o) => {
    delete e[o];
  }), delete e._chartjs);
}
function Cu(e) {
  const t = new Set(e);
  return t.size === e.length ? e : Array.from(t);
}
const Pu = function() {
  return typeof window > "u" ? function(e) {
    return e();
  } : window.requestAnimationFrame;
}();
function Tu(e, t) {
  let n = [], s = !1;
  return function(...i) {
    n = i, s || (s = !0, Pu.call(window, () => {
      s = !1, e.apply(t, n);
    }));
  };
}
function Wm(e, t) {
  let n;
  return function(...s) {
    return t ? (clearTimeout(n), n = setTimeout(e, t, s)) : e.apply(this, s), t;
  };
}
const Um = (e) => e === "start" ? "left" : e === "end" ? "right" : "center", Tl = (e, t, n) => e === "start" ? t : e === "end" ? n : (t + n) / 2, ri = (e) => e === 0 || e === 1, Al = (e, t, n) => -(Math.pow(2, 10 * (e -= 1)) * Math.sin((e - t) * Ce / n)), Vl = (e, t, n) => Math.pow(2, -10 * e) * Math.sin((e - t) * Ce / n) + 1, Ps = {
  linear: (e) => e,
  easeInQuad: (e) => e * e,
  easeOutQuad: (e) => -e * (e - 2),
  easeInOutQuad: (e) => (e /= 0.5) < 1 ? 0.5 * e * e : -0.5 * (--e * (e - 2) - 1),
  easeInCubic: (e) => e * e * e,
  easeOutCubic: (e) => (e -= 1) * e * e + 1,
  easeInOutCubic: (e) => (e /= 0.5) < 1 ? 0.5 * e * e * e : 0.5 * ((e -= 2) * e * e + 2),
  easeInQuart: (e) => e * e * e * e,
  easeOutQuart: (e) => -((e -= 1) * e * e * e - 1),
  easeInOutQuart: (e) => (e /= 0.5) < 1 ? 0.5 * e * e * e * e : -0.5 * ((e -= 2) * e * e * e - 2),
  easeInQuint: (e) => e * e * e * e * e,
  easeOutQuint: (e) => (e -= 1) * e * e * e * e + 1,
  easeInOutQuint: (e) => (e /= 0.5) < 1 ? 0.5 * e * e * e * e * e : 0.5 * ((e -= 2) * e * e * e * e + 2),
  easeInSine: (e) => -Math.cos(e * ue) + 1,
  easeOutSine: (e) => Math.sin(e * ue),
  easeInOutSine: (e) => -0.5 * (Math.cos(Vt * e) - 1),
  easeInExpo: (e) => e === 0 ? 0 : Math.pow(2, 10 * (e - 1)),
  easeOutExpo: (e) => e === 1 ? 1 : -Math.pow(2, -10 * e) + 1,
  easeInOutExpo: (e) => ri(e) ? e : e < 0.5 ? 0.5 * Math.pow(2, 10 * (e * 2 - 1)) : 0.5 * (-Math.pow(2, -10 * (e * 2 - 1)) + 2),
  easeInCirc: (e) => e >= 1 ? e : -(Math.sqrt(1 - e * e) - 1),
  easeOutCirc: (e) => Math.sqrt(1 - (e -= 1) * e),
  easeInOutCirc: (e) => (e /= 0.5) < 1 ? -0.5 * (Math.sqrt(1 - e * e) - 1) : 0.5 * (Math.sqrt(1 - (e -= 2) * e) + 1),
  easeInElastic: (e) => ri(e) ? e : Al(e, 0.075, 0.3),
  easeOutElastic: (e) => ri(e) ? e : Vl(e, 0.075, 0.3),
  easeInOutElastic(e) {
    return ri(e) ? e : e < 0.5 ? 0.5 * Al(e * 2, 0.1125, 0.45) : 0.5 + 0.5 * Vl(e * 2 - 1, 0.1125, 0.45);
  },
  easeInBack(e) {
    return e * e * ((1.70158 + 1) * e - 1.70158);
  },
  easeOutBack(e) {
    return (e -= 1) * e * ((1.70158 + 1) * e + 1.70158) + 1;
  },
  easeInOutBack(e) {
    let t = 1.70158;
    return (e /= 0.5) < 1 ? 0.5 * (e * e * (((t *= 1.525) + 1) * e - t)) : 0.5 * ((e -= 2) * e * (((t *= 1.525) + 1) * e + t) + 2);
  },
  easeInBounce: (e) => 1 - Ps.easeOutBounce(1 - e),
  easeOutBounce(e) {
    return e < 1 / 2.75 ? 7.5625 * e * e : e < 2 / 2.75 ? 7.5625 * (e -= 1.5 / 2.75) * e + 0.75 : e < 2.5 / 2.75 ? 7.5625 * (e -= 2.25 / 2.75) * e + 0.9375 : 7.5625 * (e -= 2.625 / 2.75) * e + 0.984375;
  },
  easeInOutBounce: (e) => e < 0.5 ? Ps.easeInBounce(e * 2) * 0.5 : Ps.easeOutBounce(e * 2 - 1) * 0.5 + 0.5
};
function da(e) {
  if (e && typeof e == "object") {
    const t = e.toString();
    return t === "[object CanvasPattern]" || t === "[object CanvasGradient]";
  }
  return !1;
}
function Rl(e) {
  return da(e) ? e : new Su(e);
}
function Fo(e) {
  return da(e) ? e : new Su(e).saturate(0.5).darken(0.1).hexString();
}
const Ym = [
  "x",
  "y",
  "borderWidth",
  "radius",
  "tension"
], Km = [
  "color",
  "borderColor",
  "backgroundColor"
];
function qm(e) {
  e.set("animation", {
    delay: void 0,
    duration: 1e3,
    easing: "easeOutQuart",
    fn: void 0,
    from: void 0,
    loop: void 0,
    to: void 0,
    type: void 0
  }), e.describe("animation", {
    _fallback: !1,
    _indexable: !1,
    _scriptable: (t) => t !== "onProgress" && t !== "onComplete" && t !== "fn"
  }), e.set("animations", {
    colors: {
      type: "color",
      properties: Km
    },
    numbers: {
      type: "number",
      properties: Ym
    }
  }), e.describe("animations", {
    _fallback: "animation"
  }), e.set("transitions", {
    active: {
      animation: {
        duration: 400
      }
    },
    resize: {
      animation: {
        duration: 0
      }
    },
    show: {
      animations: {
        colors: {
          from: "transparent"
        },
        visible: {
          type: "boolean",
          duration: 0
        }
      }
    },
    hide: {
      animations: {
        colors: {
          to: "transparent"
        },
        visible: {
          type: "boolean",
          easing: "linear",
          fn: (t) => t | 0
        }
      }
    }
  });
}
function Xm(e) {
  e.set("layout", {
    autoPadding: !0,
    padding: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    }
  });
}
const Il = /* @__PURE__ */ new Map();
function Gm(e, t) {
  t = t || {};
  const n = e + JSON.stringify(t);
  let s = Il.get(n);
  return s || (s = new Intl.NumberFormat(e, t), Il.set(n, s)), s;
}
function Au(e, t, n) {
  return Gm(t, n).format(e);
}
const Zm = {
  values(e) {
    return Mt(e) ? e : "" + e;
  },
  numeric(e, t, n) {
    if (e === 0)
      return "0";
    const s = this.chart.options.locale;
    let i, o = e;
    if (n.length > 1) {
      const c = Math.max(Math.abs(n[0].value), Math.abs(n[n.length - 1].value));
      (c < 1e-4 || c > 1e15) && (i = "scientific"), o = Jm(e, n);
    }
    const r = ku(Math.abs(o)), a = isNaN(r) ? 1 : Math.max(Math.min(-1 * Math.floor(r), 20), 0), l = {
      notation: i,
      minimumFractionDigits: a,
      maximumFractionDigits: a
    };
    return Object.assign(l, this.options.ticks.format), Au(e, s, l);
  }
};
function Jm(e, t) {
  let n = t.length > 3 ? t[2].value - t[1].value : t[1].value - t[0].value;
  return Math.abs(n) >= 1 && e !== Math.floor(e) && (n = e - Math.floor(e)), n;
}
var Vu = {
  formatters: Zm
};
function Qm(e) {
  e.set("scale", {
    display: !0,
    offset: !1,
    reverse: !1,
    beginAtZero: !1,
    bounds: "ticks",
    clip: !0,
    grace: 0,
    grid: {
      display: !0,
      lineWidth: 1,
      drawOnChartArea: !0,
      drawTicks: !0,
      tickLength: 8,
      tickWidth: (t, n) => n.lineWidth,
      tickColor: (t, n) => n.color,
      offset: !1
    },
    border: {
      display: !0,
      dash: [],
      dashOffset: 0,
      width: 1
    },
    title: {
      display: !1,
      text: "",
      padding: {
        top: 4,
        bottom: 4
      }
    },
    ticks: {
      minRotation: 0,
      maxRotation: 50,
      mirror: !1,
      textStrokeWidth: 0,
      textStrokeColor: "",
      padding: 3,
      display: !0,
      autoSkip: !0,
      autoSkipPadding: 3,
      labelOffset: 0,
      callback: Vu.formatters.values,
      minor: {},
      major: {},
      align: "center",
      crossAlign: "near",
      showLabelBackdrop: !1,
      backdropColor: "rgba(255, 255, 255, 0.75)",
      backdropPadding: 2
    }
  }), e.route("scale.ticks", "color", "", "color"), e.route("scale.grid", "color", "", "borderColor"), e.route("scale.border", "color", "", "borderColor"), e.route("scale.title", "color", "", "color"), e.describe("scale", {
    _fallback: !1,
    _scriptable: (t) => !t.startsWith("before") && !t.startsWith("after") && t !== "callback" && t !== "parser",
    _indexable: (t) => t !== "borderDash" && t !== "tickBorderDash" && t !== "dash"
  }), e.describe("scales", {
    _fallback: "scale"
  }), e.describe("scale.ticks", {
    _scriptable: (t) => t !== "backdropPadding" && t !== "callback",
    _indexable: (t) => t !== "backdropPadding"
  });
}
const An = /* @__PURE__ */ Object.create(null), Nr = /* @__PURE__ */ Object.create(null);
function Ts(e, t) {
  if (!t)
    return e;
  const n = t.split(".");
  for (let s = 0, i = n.length; s < i; ++s) {
    const o = n[s];
    e = e[o] || (e[o] = /* @__PURE__ */ Object.create(null));
  }
  return e;
}
function $o(e, t, n) {
  return typeof t == "string" ? Bs(Ts(e, t), n) : Bs(Ts(e, ""), t);
}
class t0 {
  constructor(t, n) {
    this.animation = void 0, this.backgroundColor = "rgba(0,0,0,0.1)", this.borderColor = "rgba(0,0,0,0.1)", this.color = "#666", this.datasets = {}, this.devicePixelRatio = (s) => s.chart.platform.getDevicePixelRatio(), this.elements = {}, this.events = [
      "mousemove",
      "mouseout",
      "click",
      "touchstart",
      "touchmove"
    ], this.font = {
      family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",
      size: 12,
      style: "normal",
      lineHeight: 1.2,
      weight: null
    }, this.hover = {}, this.hoverBackgroundColor = (s, i) => Fo(i.backgroundColor), this.hoverBorderColor = (s, i) => Fo(i.borderColor), this.hoverColor = (s, i) => Fo(i.color), this.indexAxis = "x", this.interaction = {
      mode: "nearest",
      intersect: !0,
      includeInvisible: !1
    }, this.maintainAspectRatio = !0, this.onHover = null, this.onClick = null, this.parsing = !0, this.plugins = {}, this.responsive = !0, this.scale = void 0, this.scales = {}, this.showLine = !0, this.drawActiveElementsOnTop = !0, this.describe(t), this.apply(n);
  }
  set(t, n) {
    return $o(this, t, n);
  }
  get(t) {
    return Ts(this, t);
  }
  describe(t, n) {
    return $o(Nr, t, n);
  }
  override(t, n) {
    return $o(An, t, n);
  }
  route(t, n, s, i) {
    const o = Ts(this, t), r = Ts(this, s), a = "_" + n;
    Object.defineProperties(o, {
      [a]: {
        value: o[n],
        writable: !0
      },
      [n]: {
        enumerable: !0,
        get() {
          const l = this[a], c = r[i];
          return ot(l) ? Object.assign({}, c, l) : ht(l, c);
        },
        set(l) {
          this[a] = l;
        }
      }
    });
  }
  apply(t) {
    t.forEach((n) => n(this));
  }
}
var wt = /* @__PURE__ */ new t0({
  _scriptable: (e) => !e.startsWith("on"),
  _indexable: (e) => e !== "events",
  hover: {
    _fallback: "interaction"
  },
  interaction: {
    _scriptable: !1,
    _indexable: !1
  }
}, [
  qm,
  Xm,
  Qm
]);
function e0(e) {
  return !e || gt(e.size) || gt(e.family) ? null : (e.style ? e.style + " " : "") + (e.weight ? e.weight + " " : "") + e.size + "px " + e.family;
}
function Ll(e, t, n, s, i) {
  let o = t[i];
  return o || (o = t[i] = e.measureText(i).width, n.push(i)), o > s && (s = o), s;
}
function gn(e, t, n) {
  const s = e.currentDevicePixelRatio, i = n !== 0 ? Math.max(n / 2, 0.5) : 0;
  return Math.round((t - i) * s) / s + i;
}
function Fl(e, t) {
  !t && !e || (t = t || e.getContext("2d"), t.save(), t.resetTransform(), t.clearRect(0, 0, e.width, e.height), t.restore());
}
function Dr(e, t, n, s) {
  n0(e, t, n, s);
}
function n0(e, t, n, s, i) {
  let o, r, a, l, c, f, u, h;
  const d = t.pointStyle, p = t.rotation, g = t.radius;
  let b = (p || 0) * Am;
  if (d && typeof d == "object" && (o = d.toString(), o === "[object HTMLImageElement]" || o === "[object HTMLCanvasElement]")) {
    e.save(), e.translate(n, s), e.rotate(b), e.drawImage(d, -d.width / 2, -d.height / 2, d.width, d.height), e.restore();
    return;
  }
  if (!(isNaN(g) || g <= 0)) {
    switch (e.beginPath(), d) {
      // Default includes circle
      default:
        e.arc(n, s, g, 0, Ce), e.closePath();
        break;
      case "triangle":
        f = g, e.moveTo(n + Math.sin(b) * f, s - Math.cos(b) * g), b += Nl, e.lineTo(n + Math.sin(b) * f, s - Math.cos(b) * g), b += Nl, e.lineTo(n + Math.sin(b) * f, s - Math.cos(b) * g), e.closePath();
        break;
      case "rectRounded":
        c = g * 0.516, l = g - c, r = Math.cos(b + pn) * l, u = Math.cos(b + pn) * l, a = Math.sin(b + pn) * l, h = Math.sin(b + pn) * l, e.arc(n - u, s - a, c, b - Vt, b - ue), e.arc(n + h, s - r, c, b - ue, b), e.arc(n + u, s + a, c, b, b + ue), e.arc(n - h, s + r, c, b + ue, b + Vt), e.closePath();
        break;
      case "rect":
        if (!p) {
          l = Math.SQRT1_2 * g, f = l, e.rect(n - f, s - l, 2 * f, 2 * l);
          break;
        }
        b += pn;
      /* falls through */
      case "rectRot":
        u = Math.cos(b) * g, r = Math.cos(b) * g, a = Math.sin(b) * g, h = Math.sin(b) * g, e.moveTo(n - u, s - a), e.lineTo(n + h, s - r), e.lineTo(n + u, s + a), e.lineTo(n - h, s + r), e.closePath();
        break;
      case "crossRot":
        b += pn;
      /* falls through */
      case "cross":
        u = Math.cos(b) * g, r = Math.cos(b) * g, a = Math.sin(b) * g, h = Math.sin(b) * g, e.moveTo(n - u, s - a), e.lineTo(n + u, s + a), e.moveTo(n + h, s - r), e.lineTo(n - h, s + r);
        break;
      case "star":
        u = Math.cos(b) * g, r = Math.cos(b) * g, a = Math.sin(b) * g, h = Math.sin(b) * g, e.moveTo(n - u, s - a), e.lineTo(n + u, s + a), e.moveTo(n + h, s - r), e.lineTo(n - h, s + r), b += pn, u = Math.cos(b) * g, r = Math.cos(b) * g, a = Math.sin(b) * g, h = Math.sin(b) * g, e.moveTo(n - u, s - a), e.lineTo(n + u, s + a), e.moveTo(n + h, s - r), e.lineTo(n - h, s + r);
        break;
      case "line":
        r = Math.cos(b) * g, a = Math.sin(b) * g, e.moveTo(n - r, s - a), e.lineTo(n + r, s + a);
        break;
      case "dash":
        e.moveTo(n, s), e.lineTo(n + Math.cos(b) * g, s + Math.sin(b) * g);
        break;
      case !1:
        e.closePath();
        break;
    }
    e.fill(), t.borderWidth > 0 && e.stroke();
  }
}
function zs(e, t, n) {
  return n = n || 0.5, !t || e && e.x > t.left - n && e.x < t.right + n && e.y > t.top - n && e.y < t.bottom + n;
}
function pa(e, t) {
  e.save(), e.beginPath(), e.rect(t.left, t.top, t.right - t.left, t.bottom - t.top), e.clip();
}
function ga(e) {
  e.restore();
}
function s0(e, t, n, s, i) {
  if (!t)
    return e.lineTo(n.x, n.y);
  if (i === "middle") {
    const o = (t.x + n.x) / 2;
    e.lineTo(o, t.y), e.lineTo(o, n.y);
  } else i === "after" != !!s ? e.lineTo(t.x, n.y) : e.lineTo(n.x, t.y);
  e.lineTo(n.x, n.y);
}
function i0(e, t, n, s) {
  if (!t)
    return e.lineTo(n.x, n.y);
  e.bezierCurveTo(s ? t.cp1x : t.cp2x, s ? t.cp1y : t.cp2y, s ? n.cp2x : n.cp1x, s ? n.cp2y : n.cp1y, n.x, n.y);
}
function o0(e, t) {
  t.translation && e.translate(t.translation[0], t.translation[1]), gt(t.rotation) || e.rotate(t.rotation), t.color && (e.fillStyle = t.color), t.textAlign && (e.textAlign = t.textAlign), t.textBaseline && (e.textBaseline = t.textBaseline);
}
function r0(e, t, n, s, i) {
  if (i.strikethrough || i.underline) {
    const o = e.measureText(s), r = t - o.actualBoundingBoxLeft, a = t + o.actualBoundingBoxRight, l = n - o.actualBoundingBoxAscent, c = n + o.actualBoundingBoxDescent, f = i.strikethrough ? (l + c) / 2 : c;
    e.strokeStyle = e.fillStyle, e.beginPath(), e.lineWidth = i.decorationWidth || 2, e.moveTo(r, f), e.lineTo(a, f), e.stroke();
  }
}
function a0(e, t) {
  const n = e.fillStyle;
  e.fillStyle = t.color, e.fillRect(t.left, t.top, t.width, t.height), e.fillStyle = n;
}
function $l(e, t, n, s, i, o = {}) {
  const r = Mt(t) ? t : [
    t
  ], a = o.strokeWidth > 0 && o.strokeColor !== "";
  let l, c;
  for (e.save(), e.font = i.string, o0(e, o), l = 0; l < r.length; ++l)
    c = r[l], o.backdrop && a0(e, o.backdrop), a && (o.strokeColor && (e.strokeStyle = o.strokeColor), gt(o.strokeWidth) || (e.lineWidth = o.strokeWidth), e.strokeText(c, n, s, o.maxWidth)), e.fillText(c, n, s, o.maxWidth), r0(e, n, s, c, o), s += Number(i.lineHeight);
  e.restore();
}
function Cr(e, t) {
  const { x: n, y: s, w: i, h: o, radius: r } = t;
  e.arc(n + r.topLeft, s + r.topLeft, r.topLeft, 1.5 * Vt, Vt, !0), e.lineTo(n, s + o - r.bottomLeft), e.arc(n + r.bottomLeft, s + o - r.bottomLeft, r.bottomLeft, Vt, ue, !0), e.lineTo(n + i - r.bottomRight, s + o), e.arc(n + i - r.bottomRight, s + o - r.bottomRight, r.bottomRight, ue, 0, !0), e.lineTo(n + i, s + r.topRight), e.arc(n + i - r.topRight, s + r.topRight, r.topRight, 0, -ue, !0), e.lineTo(n + r.topLeft, s);
}
const l0 = /^(normal|(\d+(?:\.\d+)?)(px|em|%)?)$/, c0 = /^(normal|italic|initial|inherit|unset|(oblique( -?[0-9]?[0-9]deg)?))$/;
function f0(e, t) {
  const n = ("" + e).match(l0);
  if (!n || n[1] === "normal")
    return t * 1.2;
  switch (e = +n[2], n[3]) {
    case "px":
      return e;
    case "%":
      e /= 100;
      break;
  }
  return t * e;
}
const u0 = (e) => +e || 0;
function Ru(e, t) {
  const n = {}, s = ot(t), i = s ? Object.keys(t) : t, o = ot(e) ? s ? (r) => ht(e[r], e[t[r]]) : (r) => e[r] : () => e;
  for (const r of i)
    n[r] = u0(o(r));
  return n;
}
function Iu(e) {
  return Ru(e, {
    top: "y",
    right: "x",
    bottom: "y",
    left: "x"
  });
}
function As(e) {
  return Ru(e, [
    "topLeft",
    "topRight",
    "bottomLeft",
    "bottomRight"
  ]);
}
function an(e) {
  const t = Iu(e);
  return t.width = t.left + t.right, t.height = t.top + t.bottom, t;
}
function Ne(e, t) {
  e = e || {}, t = t || wt.font;
  let n = ht(e.size, t.size);
  typeof n == "string" && (n = parseInt(n, 10));
  let s = ht(e.style, t.style);
  s && !("" + s).match(c0) && (console.warn('Invalid font style specified: "' + s + '"'), s = void 0);
  const i = {
    family: ht(e.family, t.family),
    lineHeight: f0(ht(e.lineHeight, t.lineHeight), n),
    size: n,
    style: s,
    weight: ht(e.weight, t.weight),
    string: ""
  };
  return i.string = e0(i), i;
}
function ai(e, t, n, s) {
  let i, o, r;
  for (i = 0, o = e.length; i < o; ++i)
    if (r = e[i], r !== void 0 && r !== void 0)
      return r;
}
function h0(e, t, n) {
  const { min: s, max: i } = e, o = Mm(t, (i - s) / 2), r = (a, l) => n && a === 0 ? 0 : a + l;
  return {
    min: r(s, -Math.abs(o)),
    max: r(i, o)
  };
}
function Vn(e, t) {
  return Object.assign(Object.create(e), t);
}
function ma(e, t = [
  ""
], n, s, i = () => e[0]) {
  const o = n || e;
  typeof s > "u" && (s = Bu("_fallback", e));
  const r = {
    [Symbol.toStringTag]: "Object",
    _cacheable: !0,
    _scopes: e,
    _rootScopes: o,
    _fallback: s,
    _getTarget: i,
    override: (a) => ma([
      a,
      ...e
    ], t, o, s)
  };
  return new Proxy(r, {
    /**
    * A trap for the delete operator.
    */
    deleteProperty(a, l) {
      return delete a[l], delete a._keys, delete e[0][l], !0;
    },
    /**
    * A trap for getting property values.
    */
    get(a, l) {
      return Fu(a, l, () => x0(l, t, e, a));
    },
    /**
    * A trap for Object.getOwnPropertyDescriptor.
    * Also used by Object.hasOwnProperty.
    */
    getOwnPropertyDescriptor(a, l) {
      return Reflect.getOwnPropertyDescriptor(a._scopes[0], l);
    },
    /**
    * A trap for Object.getPrototypeOf.
    */
    getPrototypeOf() {
      return Reflect.getPrototypeOf(e[0]);
    },
    /**
    * A trap for the in operator.
    */
    has(a, l) {
      return jl(a).includes(l);
    },
    /**
    * A trap for Object.getOwnPropertyNames and Object.getOwnPropertySymbols.
    */
    ownKeys(a) {
      return jl(a);
    },
    /**
    * A trap for setting property values.
    */
    set(a, l, c) {
      const f = a._storage || (a._storage = i());
      return a[l] = f[l] = c, delete a._keys, !0;
    }
  });
}
function qn(e, t, n, s) {
  const i = {
    _cacheable: !1,
    _proxy: e,
    _context: t,
    _subProxy: n,
    _stack: /* @__PURE__ */ new Set(),
    _descriptors: Lu(e, s),
    setContext: (o) => qn(e, o, n, s),
    override: (o) => qn(e.override(o), t, n, s)
  };
  return new Proxy(i, {
    /**
    * A trap for the delete operator.
    */
    deleteProperty(o, r) {
      return delete o[r], delete e[r], !0;
    },
    /**
    * A trap for getting property values.
    */
    get(o, r, a) {
      return Fu(o, r, () => p0(o, r, a));
    },
    /**
    * A trap for Object.getOwnPropertyDescriptor.
    * Also used by Object.hasOwnProperty.
    */
    getOwnPropertyDescriptor(o, r) {
      return o._descriptors.allKeys ? Reflect.has(e, r) ? {
        enumerable: !0,
        configurable: !0
      } : void 0 : Reflect.getOwnPropertyDescriptor(e, r);
    },
    /**
    * A trap for Object.getPrototypeOf.
    */
    getPrototypeOf() {
      return Reflect.getPrototypeOf(e);
    },
    /**
    * A trap for the in operator.
    */
    has(o, r) {
      return Reflect.has(e, r);
    },
    /**
    * A trap for Object.getOwnPropertyNames and Object.getOwnPropertySymbols.
    */
    ownKeys() {
      return Reflect.ownKeys(e);
    },
    /**
    * A trap for setting property values.
    */
    set(o, r, a) {
      return e[r] = a, delete o[r], !0;
    }
  });
}
function Lu(e, t = {
  scriptable: !0,
  indexable: !0
}) {
  const { _scriptable: n = t.scriptable, _indexable: s = t.indexable, _allKeys: i = t.allKeys } = e;
  return {
    allKeys: i,
    scriptable: n,
    indexable: s,
    isScriptable: rn(n) ? n : () => n,
    isIndexable: rn(s) ? s : () => s
  };
}
const d0 = (e, t) => e ? e + ua(t) : t, ba = (e, t) => ot(t) && e !== "adapters" && (Object.getPrototypeOf(t) === null || t.constructor === Object);
function Fu(e, t, n) {
  if (Object.prototype.hasOwnProperty.call(e, t) || t === "constructor")
    return e[t];
  const s = n();
  return e[t] = s, s;
}
function p0(e, t, n) {
  const { _proxy: s, _context: i, _subProxy: o, _descriptors: r } = e;
  let a = s[t];
  return rn(a) && r.isScriptable(t) && (a = g0(t, a, e, n)), Mt(a) && a.length && (a = m0(t, a, e, r.isIndexable)), ba(t, a) && (a = qn(a, i, o && o[t], r)), a;
}
function g0(e, t, n, s) {
  const { _proxy: i, _context: o, _subProxy: r, _stack: a } = n;
  if (a.has(e))
    throw new Error("Recursion detected: " + Array.from(a).join("->") + "->" + e);
  a.add(e);
  let l = t(o, r || s);
  return a.delete(e), ba(e, l) && (l = _a(i._scopes, i, e, l)), l;
}
function m0(e, t, n, s) {
  const { _proxy: i, _context: o, _subProxy: r, _descriptors: a } = n;
  if (typeof o.index < "u" && s(e))
    return t[o.index % t.length];
  if (ot(t[0])) {
    const l = t, c = i._scopes.filter((f) => f !== l);
    t = [];
    for (const f of l) {
      const u = _a(c, i, e, f);
      t.push(qn(u, o, r && r[e], a));
    }
  }
  return t;
}
function $u(e, t, n) {
  return rn(e) ? e(t, n) : e;
}
const b0 = (e, t) => e === !0 ? t : typeof e == "string" ? Kn(t, e) : void 0;
function _0(e, t, n, s, i) {
  for (const o of t) {
    const r = b0(n, o);
    if (r) {
      e.add(r);
      const a = $u(r._fallback, n, i);
      if (typeof a < "u" && a !== n && a !== s)
        return a;
    } else if (r === !1 && typeof s < "u" && n !== s)
      return null;
  }
  return !1;
}
function _a(e, t, n, s) {
  const i = t._rootScopes, o = $u(t._fallback, n, s), r = [
    ...e,
    ...i
  ], a = /* @__PURE__ */ new Set();
  a.add(s);
  let l = Bl(a, r, n, o || n, s);
  return l === null || typeof o < "u" && o !== n && (l = Bl(a, r, o, l, s), l === null) ? !1 : ma(Array.from(a), [
    ""
  ], i, o, () => y0(t, n, s));
}
function Bl(e, t, n, s, i) {
  for (; n; )
    n = _0(e, t, n, s, i);
  return n;
}
function y0(e, t, n) {
  const s = e._getTarget();
  t in s || (s[t] = {});
  const i = s[t];
  return Mt(i) && ot(n) ? n : i || {};
}
function x0(e, t, n, s) {
  let i;
  for (const o of t)
    if (i = Bu(d0(o, e), n), typeof i < "u")
      return ba(e, i) ? _a(n, s, e, i) : i;
}
function Bu(e, t) {
  for (const n of t) {
    if (!n)
      continue;
    const s = n[e];
    if (typeof s < "u")
      return s;
  }
}
function jl(e) {
  let t = e._keys;
  return t || (t = e._keys = v0(e._scopes)), t;
}
function v0(e) {
  const t = /* @__PURE__ */ new Set();
  for (const n of e)
    for (const s of Object.keys(n).filter((i) => !i.startsWith("_")))
      t.add(s);
  return Array.from(t);
}
const w0 = Number.EPSILON || 1e-14, Xn = (e, t) => t < e.length && !e[t].skip && e[t], ju = (e) => e === "x" ? "y" : "x";
function E0(e, t, n, s) {
  const i = e.skip ? t : e, o = t, r = n.skip ? t : n, a = Mr(o, i), l = Mr(r, o);
  let c = a / (a + l), f = l / (a + l);
  c = isNaN(c) ? 0 : c, f = isNaN(f) ? 0 : f;
  const u = s * c, h = s * f;
  return {
    previous: {
      x: o.x - u * (r.x - i.x),
      y: o.y - u * (r.y - i.y)
    },
    next: {
      x: o.x + h * (r.x - i.x),
      y: o.y + h * (r.y - i.y)
    }
  };
}
function O0(e, t, n) {
  const s = e.length;
  let i, o, r, a, l, c = Xn(e, 0);
  for (let f = 0; f < s - 1; ++f)
    if (l = c, c = Xn(e, f + 1), !(!l || !c)) {
      if (Cs(t[f], 0, w0)) {
        n[f] = n[f + 1] = 0;
        continue;
      }
      i = n[f] / t[f], o = n[f + 1] / t[f], a = Math.pow(i, 2) + Math.pow(o, 2), !(a <= 9) && (r = 3 / Math.sqrt(a), n[f] = i * r * t[f], n[f + 1] = o * r * t[f]);
    }
}
function S0(e, t, n = "x") {
  const s = ju(n), i = e.length;
  let o, r, a, l = Xn(e, 0);
  for (let c = 0; c < i; ++c) {
    if (r = a, a = l, l = Xn(e, c + 1), !a)
      continue;
    const f = a[n], u = a[s];
    r && (o = (f - r[n]) / 3, a[`cp1${n}`] = f - o, a[`cp1${s}`] = u - o * t[c]), l && (o = (l[n] - f) / 3, a[`cp2${n}`] = f + o, a[`cp2${s}`] = u + o * t[c]);
  }
}
function M0(e, t = "x") {
  const n = ju(t), s = e.length, i = Array(s).fill(0), o = Array(s);
  let r, a, l, c = Xn(e, 0);
  for (r = 0; r < s; ++r)
    if (a = l, l = c, c = Xn(e, r + 1), !!l) {
      if (c) {
        const f = c[t] - l[t];
        i[r] = f !== 0 ? (c[n] - l[n]) / f : 0;
      }
      o[r] = a ? c ? Pe(i[r - 1]) !== Pe(i[r]) ? 0 : (i[r - 1] + i[r]) / 2 : i[r - 1] : i[r];
    }
  O0(e, i, o), S0(e, o, t);
}
function li(e, t, n) {
  return Math.max(Math.min(e, n), t);
}
function k0(e, t) {
  let n, s, i, o, r, a = zs(e[0], t);
  for (n = 0, s = e.length; n < s; ++n)
    r = o, o = a, a = n < s - 1 && zs(e[n + 1], t), o && (i = e[n], r && (i.cp1x = li(i.cp1x, t.left, t.right), i.cp1y = li(i.cp1y, t.top, t.bottom)), a && (i.cp2x = li(i.cp2x, t.left, t.right), i.cp2y = li(i.cp2y, t.top, t.bottom)));
}
function N0(e, t, n, s, i) {
  let o, r, a, l;
  if (t.spanGaps && (e = e.filter((c) => !c.skip)), t.cubicInterpolationMode === "monotone")
    M0(e, i);
  else {
    let c = s ? e[e.length - 1] : e[0];
    for (o = 0, r = e.length; o < r; ++o)
      a = e[o], l = E0(c, a, e[Math.min(o + 1, r - (s ? 0 : 1)) % r], t.tension), a.cp1x = l.previous.x, a.cp1y = l.previous.y, a.cp2x = l.next.x, a.cp2y = l.next.y, c = a;
  }
  t.capBezierPoints && k0(e, n);
}
function ya() {
  return typeof window < "u" && typeof document < "u";
}
function xa(e) {
  let t = e.parentNode;
  return t && t.toString() === "[object ShadowRoot]" && (t = t.host), t;
}
function Qi(e, t, n) {
  let s;
  return typeof e == "string" ? (s = parseInt(e, 10), e.indexOf("%") !== -1 && (s = s / 100 * t.parentNode[n])) : s = e, s;
}
const yo = (e) => e.ownerDocument.defaultView.getComputedStyle(e, null);
function D0(e, t) {
  return yo(e).getPropertyValue(t);
}
const C0 = [
  "top",
  "right",
  "bottom",
  "left"
];
function Cn(e, t, n) {
  const s = {};
  n = n ? "-" + n : "";
  for (let i = 0; i < 4; i++) {
    const o = C0[i];
    s[o] = parseFloat(e[t + "-" + o + n]) || 0;
  }
  return s.width = s.left + s.right, s.height = s.top + s.bottom, s;
}
const P0 = (e, t, n) => (e > 0 || t > 0) && (!n || !n.shadowRoot);
function T0(e, t) {
  const n = e.touches, s = n && n.length ? n[0] : e, { offsetX: i, offsetY: o } = s;
  let r = !1, a, l;
  if (P0(i, o, e.target))
    a = i, l = o;
  else {
    const c = t.getBoundingClientRect();
    a = s.clientX - c.left, l = s.clientY - c.top, r = !0;
  }
  return {
    x: a,
    y: l,
    box: r
  };
}
function yn(e, t) {
  if ("native" in e)
    return e;
  const { canvas: n, currentDevicePixelRatio: s } = t, i = yo(n), o = i.boxSizing === "border-box", r = Cn(i, "padding"), a = Cn(i, "border", "width"), { x: l, y: c, box: f } = T0(e, n), u = r.left + (f && a.left), h = r.top + (f && a.top);
  let { width: d, height: p } = t;
  return o && (d -= r.width + a.width, p -= r.height + a.height), {
    x: Math.round((l - u) / d * n.width / s),
    y: Math.round((c - h) / p * n.height / s)
  };
}
function A0(e, t, n) {
  let s, i;
  if (t === void 0 || n === void 0) {
    const o = e && xa(e);
    if (!o)
      t = e.clientWidth, n = e.clientHeight;
    else {
      const r = o.getBoundingClientRect(), a = yo(o), l = Cn(a, "border", "width"), c = Cn(a, "padding");
      t = r.width - c.width - l.width, n = r.height - c.height - l.height, s = Qi(a.maxWidth, o, "clientWidth"), i = Qi(a.maxHeight, o, "clientHeight");
    }
  }
  return {
    width: t,
    height: n,
    maxWidth: s || Gi,
    maxHeight: i || Gi
  };
}
const ci = (e) => Math.round(e * 10) / 10;
function V0(e, t, n, s) {
  const i = yo(e), o = Cn(i, "margin"), r = Qi(i.maxWidth, e, "clientWidth") || Gi, a = Qi(i.maxHeight, e, "clientHeight") || Gi, l = A0(e, t, n);
  let { width: c, height: f } = l;
  if (i.boxSizing === "content-box") {
    const h = Cn(i, "border", "width"), d = Cn(i, "padding");
    c -= d.width + h.width, f -= d.height + h.height;
  }
  return c = Math.max(0, c - o.width), f = Math.max(0, s ? c / s : f - o.height), c = ci(Math.min(c, r, l.maxWidth)), f = ci(Math.min(f, a, l.maxHeight)), c && !f && (f = ci(c / 2)), (t !== void 0 || n !== void 0) && s && l.height && f > l.height && (f = l.height, c = ci(Math.floor(f * s))), {
    width: c,
    height: f
  };
}
function zl(e, t, n) {
  const s = t || 1, i = Math.floor(e.height * s), o = Math.floor(e.width * s);
  e.height = Math.floor(e.height), e.width = Math.floor(e.width);
  const r = e.canvas;
  return r.style && (n || !r.style.height && !r.style.width) && (r.style.height = `${e.height}px`, r.style.width = `${e.width}px`), e.currentDevicePixelRatio !== s || r.height !== i || r.width !== o ? (e.currentDevicePixelRatio = s, r.height = i, r.width = o, e.ctx.setTransform(s, 0, 0, s, 0, 0), !0) : !1;
}
const R0 = function() {
  let e = !1;
  try {
    const t = {
      get passive() {
        return e = !0, !1;
      }
    };
    ya() && (window.addEventListener("test", null, t), window.removeEventListener("test", null, t));
  } catch {
  }
  return e;
}();
function Hl(e, t) {
  const n = D0(e, t), s = n && n.match(/^(\d+)(\.\d+)?px$/);
  return s ? +s[1] : void 0;
}
function xn(e, t, n, s) {
  return {
    x: e.x + n * (t.x - e.x),
    y: e.y + n * (t.y - e.y)
  };
}
function I0(e, t, n, s) {
  return {
    x: e.x + n * (t.x - e.x),
    y: s === "middle" ? n < 0.5 ? e.y : t.y : s === "after" ? n < 1 ? e.y : t.y : n > 0 ? t.y : e.y
  };
}
function L0(e, t, n, s) {
  const i = {
    x: e.cp2x,
    y: e.cp2y
  }, o = {
    x: t.cp1x,
    y: t.cp1y
  }, r = xn(e, i, n), a = xn(i, o, n), l = xn(o, t, n), c = xn(r, a, n), f = xn(a, l, n);
  return xn(c, f, n);
}
const F0 = function(e, t) {
  return {
    x(n) {
      return e + e + t - n;
    },
    setWidth(n) {
      t = n;
    },
    textAlign(n) {
      return n === "center" ? n : n === "right" ? "left" : "right";
    },
    xPlus(n, s) {
      return n - s;
    },
    leftForLtr(n, s) {
      return n - s;
    }
  };
}, $0 = function() {
  return {
    x(e) {
      return e;
    },
    setWidth(e) {
    },
    textAlign(e) {
      return e;
    },
    xPlus(e, t) {
      return e + t;
    },
    leftForLtr(e, t) {
      return e;
    }
  };
};
function Bo(e, t, n) {
  return e ? F0(t, n) : $0();
}
function B0(e, t) {
  let n, s;
  (t === "ltr" || t === "rtl") && (n = e.canvas.style, s = [
    n.getPropertyValue("direction"),
    n.getPropertyPriority("direction")
  ], n.setProperty("direction", t, "important"), e.prevTextDirection = s);
}
function j0(e, t) {
  t !== void 0 && (delete e.prevTextDirection, e.canvas.style.setProperty("direction", t[0], t[1]));
}
function zu(e) {
  return e === "angle" ? {
    between: Nu,
    compare: $m,
    normalize: Oe
  } : {
    between: Ji,
    compare: (t, n) => t - n,
    normalize: (t) => t
  };
}
function Wl({ start: e, end: t, count: n, loop: s, style: i }) {
  return {
    start: e % n,
    end: t % n,
    loop: s && (t - e + 1) % n === 0,
    style: i
  };
}
function z0(e, t, n) {
  const { property: s, start: i, end: o } = n, { between: r, normalize: a } = zu(s), l = t.length;
  let { start: c, end: f, loop: u } = e, h, d;
  if (u) {
    for (c += l, f += l, h = 0, d = l; h < d && r(a(t[c % l][s]), i, o); ++h)
      c--, f--;
    c %= l, f %= l;
  }
  return f < c && (f += l), {
    start: c,
    end: f,
    loop: u,
    style: e.style
  };
}
function Hu(e, t, n) {
  if (!n)
    return [
      e
    ];
  const { property: s, start: i, end: o } = n, r = t.length, { compare: a, between: l, normalize: c } = zu(s), { start: f, end: u, loop: h, style: d } = z0(e, t, n), p = [];
  let g = !1, b = null, y, O, M;
  const P = () => l(i, M, y) && a(i, M) !== 0, w = () => a(o, y) === 0 || l(o, M, y), k = () => g || P(), v = () => !g || w();
  for (let S = f, D = f; S <= u; ++S)
    O = t[S % r], !O.skip && (y = c(O[s]), y !== M && (g = l(y, i, o), b === null && k() && (b = a(y, i) === 0 ? S : D), b !== null && v() && (p.push(Wl({
      start: b,
      end: S,
      loop: h,
      count: r,
      style: d
    })), b = null), D = S, M = y));
  return b !== null && p.push(Wl({
    start: b,
    end: u,
    loop: h,
    count: r,
    style: d
  })), p;
}
function Wu(e, t) {
  const n = [], s = e.segments;
  for (let i = 0; i < s.length; i++) {
    const o = Hu(s[i], e.points, t);
    o.length && n.push(...o);
  }
  return n;
}
function H0(e, t, n, s) {
  let i = 0, o = t - 1;
  if (n && !s)
    for (; i < t && !e[i].skip; )
      i++;
  for (; i < t && e[i].skip; )
    i++;
  for (i %= t, n && (o += i); o > i && e[o % t].skip; )
    o--;
  return o %= t, {
    start: i,
    end: o
  };
}
function W0(e, t, n, s) {
  const i = e.length, o = [];
  let r = t, a = e[t], l;
  for (l = t + 1; l <= n; ++l) {
    const c = e[l % i];
    c.skip || c.stop ? a.skip || (s = !1, o.push({
      start: t % i,
      end: (l - 1) % i,
      loop: s
    }), t = r = c.stop ? l : null) : (r = l, a.skip && (t = l)), a = c;
  }
  return r !== null && o.push({
    start: t % i,
    end: r % i,
    loop: s
  }), o;
}
function U0(e, t) {
  const n = e.points, s = e.options.spanGaps, i = n.length;
  if (!i)
    return [];
  const o = !!e._loop, { start: r, end: a } = H0(n, i, o, s);
  if (s === !0)
    return Ul(e, [
      {
        start: r,
        end: a,
        loop: o
      }
    ], n, t);
  const l = a < r ? a + i : a, c = !!e._fullLoop && r === 0 && a === i - 1;
  return Ul(e, W0(n, r, l, c), n, t);
}
function Ul(e, t, n, s) {
  return !s || !s.setContext || !n ? t : Y0(e, t, n, s);
}
function Y0(e, t, n, s) {
  const i = e._chart.getContext(), o = Yl(e.options), { _datasetIndex: r, options: { spanGaps: a } } = e, l = n.length, c = [];
  let f = o, u = t[0].start, h = u;
  function d(p, g, b, y) {
    const O = a ? -1 : 1;
    if (p !== g) {
      for (p += l; n[p % l].skip; )
        p -= O;
      for (; n[g % l].skip; )
        g += O;
      p % l !== g % l && (c.push({
        start: p % l,
        end: g % l,
        loop: b,
        style: y
      }), f = y, u = g % l);
    }
  }
  for (const p of t) {
    u = a ? u : p.start;
    let g = n[u % l], b;
    for (h = u + 1; h <= p.end; h++) {
      const y = n[h % l];
      b = Yl(s.setContext(Vn(i, {
        type: "segment",
        p0: g,
        p1: y,
        p0DataIndex: (h - 1) % l,
        p1DataIndex: h % l,
        datasetIndex: r
      }))), K0(b, f) && d(u, h - 1, p.loop, f), g = y, f = b;
    }
    u < h - 1 && d(u, h - 1, p.loop, f);
  }
  return c;
}
function Yl(e) {
  return {
    backgroundColor: e.backgroundColor,
    borderCapStyle: e.borderCapStyle,
    borderDash: e.borderDash,
    borderDashOffset: e.borderDashOffset,
    borderJoinStyle: e.borderJoinStyle,
    borderWidth: e.borderWidth,
    borderColor: e.borderColor
  };
}
function K0(e, t) {
  if (!t)
    return !1;
  const n = [], s = function(i, o) {
    return da(o) ? (n.includes(o) || n.push(o), n.indexOf(o)) : o;
  };
  return JSON.stringify(e, s) !== JSON.stringify(t, s);
}
/*!
 * Chart.js v4.4.7
 * https://www.chartjs.org
 * (c) 2024 Chart.js Contributors
 * Released under the MIT License
 */
class q0 {
  constructor() {
    this._request = null, this._charts = /* @__PURE__ */ new Map(), this._running = !1, this._lastDate = void 0;
  }
  _notify(t, n, s, i) {
    const o = n.listeners[i], r = n.duration;
    o.forEach((a) => a({
      chart: t,
      initial: n.initial,
      numSteps: r,
      currentStep: Math.min(s - n.start, r)
    }));
  }
  _refresh() {
    this._request || (this._running = !0, this._request = Pu.call(window, () => {
      this._update(), this._request = null, this._running && this._refresh();
    }));
  }
  _update(t = Date.now()) {
    let n = 0;
    this._charts.forEach((s, i) => {
      if (!s.running || !s.items.length)
        return;
      const o = s.items;
      let r = o.length - 1, a = !1, l;
      for (; r >= 0; --r)
        l = o[r], l._active ? (l._total > s.duration && (s.duration = l._total), l.tick(t), a = !0) : (o[r] = o[o.length - 1], o.pop());
      a && (i.draw(), this._notify(i, s, t, "progress")), o.length || (s.running = !1, this._notify(i, s, t, "complete"), s.initial = !1), n += o.length;
    }), this._lastDate = t, n === 0 && (this._running = !1);
  }
  _getAnims(t) {
    const n = this._charts;
    let s = n.get(t);
    return s || (s = {
      running: !1,
      initial: !0,
      items: [],
      listeners: {
        complete: [],
        progress: []
      }
    }, n.set(t, s)), s;
  }
  listen(t, n, s) {
    this._getAnims(t).listeners[n].push(s);
  }
  add(t, n) {
    !n || !n.length || this._getAnims(t).items.push(...n);
  }
  has(t) {
    return this._getAnims(t).items.length > 0;
  }
  start(t) {
    const n = this._charts.get(t);
    n && (n.running = !0, n.start = Date.now(), n.duration = n.items.reduce((s, i) => Math.max(s, i._duration), 0), this._refresh());
  }
  running(t) {
    if (!this._running)
      return !1;
    const n = this._charts.get(t);
    return !(!n || !n.running || !n.items.length);
  }
  stop(t) {
    const n = this._charts.get(t);
    if (!n || !n.items.length)
      return;
    const s = n.items;
    let i = s.length - 1;
    for (; i >= 0; --i)
      s[i].cancel();
    n.items = [], this._notify(t, n, Date.now(), "complete");
  }
  remove(t) {
    return this._charts.delete(t);
  }
}
var $e = /* @__PURE__ */ new q0();
const Kl = "transparent", X0 = {
  boolean(e, t, n) {
    return n > 0.5 ? t : e;
  },
  color(e, t, n) {
    const s = Rl(e || Kl), i = s.valid && Rl(t || Kl);
    return i && i.valid ? i.mix(s, n).hexString() : t;
  },
  number(e, t, n) {
    return e + (t - e) * n;
  }
};
class G0 {
  constructor(t, n, s, i) {
    const o = n[s];
    i = ai([
      t.to,
      i,
      o,
      t.from
    ]);
    const r = ai([
      t.from,
      o,
      i
    ]);
    this._active = !0, this._fn = t.fn || X0[t.type || typeof r], this._easing = Ps[t.easing] || Ps.linear, this._start = Math.floor(Date.now() + (t.delay || 0)), this._duration = this._total = Math.floor(t.duration), this._loop = !!t.loop, this._target = n, this._prop = s, this._from = r, this._to = i, this._promises = void 0;
  }
  active() {
    return this._active;
  }
  update(t, n, s) {
    if (this._active) {
      this._notify(!1);
      const i = this._target[this._prop], o = s - this._start, r = this._duration - o;
      this._start = s, this._duration = Math.floor(Math.max(r, t.duration)), this._total += o, this._loop = !!t.loop, this._to = ai([
        t.to,
        n,
        i,
        t.from
      ]), this._from = ai([
        t.from,
        i,
        n
      ]);
    }
  }
  cancel() {
    this._active && (this.tick(Date.now()), this._active = !1, this._notify(!1));
  }
  tick(t) {
    const n = t - this._start, s = this._duration, i = this._prop, o = this._from, r = this._loop, a = this._to;
    let l;
    if (this._active = o !== a && (r || n < s), !this._active) {
      this._target[i] = a, this._notify(!0);
      return;
    }
    if (n < 0) {
      this._target[i] = o;
      return;
    }
    l = n / s % 2, l = r && l > 1 ? 2 - l : l, l = this._easing(Math.min(1, Math.max(0, l))), this._target[i] = this._fn(o, a, l);
  }
  wait() {
    const t = this._promises || (this._promises = []);
    return new Promise((n, s) => {
      t.push({
        res: n,
        rej: s
      });
    });
  }
  _notify(t) {
    const n = t ? "res" : "rej", s = this._promises || [];
    for (let i = 0; i < s.length; i++)
      s[i][n]();
  }
}
class Uu {
  constructor(t, n) {
    this._chart = t, this._properties = /* @__PURE__ */ new Map(), this.configure(n);
  }
  configure(t) {
    if (!ot(t))
      return;
    const n = Object.keys(wt.animation), s = this._properties;
    Object.getOwnPropertyNames(t).forEach((i) => {
      const o = t[i];
      if (!ot(o))
        return;
      const r = {};
      for (const a of n)
        r[a] = o[a];
      (Mt(o.properties) && o.properties || [
        i
      ]).forEach((a) => {
        (a === i || !s.has(a)) && s.set(a, r);
      });
    });
  }
  _animateOptions(t, n) {
    const s = n.options, i = J0(t, s);
    if (!i)
      return [];
    const o = this._createAnimations(i, s);
    return s.$shared && Z0(t.options.$animations, s).then(() => {
      t.options = s;
    }, () => {
    }), o;
  }
  _createAnimations(t, n) {
    const s = this._properties, i = [], o = t.$animations || (t.$animations = {}), r = Object.keys(n), a = Date.now();
    let l;
    for (l = r.length - 1; l >= 0; --l) {
      const c = r[l];
      if (c.charAt(0) === "$")
        continue;
      if (c === "options") {
        i.push(...this._animateOptions(t, n));
        continue;
      }
      const f = n[c];
      let u = o[c];
      const h = s.get(c);
      if (u)
        if (h && u.active()) {
          u.update(h, f, a);
          continue;
        } else
          u.cancel();
      if (!h || !h.duration) {
        t[c] = f;
        continue;
      }
      o[c] = u = new G0(h, t, c, f), i.push(u);
    }
    return i;
  }
  update(t, n) {
    if (this._properties.size === 0) {
      Object.assign(t, n);
      return;
    }
    const s = this._createAnimations(t, n);
    if (s.length)
      return $e.add(this._chart, s), !0;
  }
}
function Z0(e, t) {
  const n = [], s = Object.keys(t);
  for (let i = 0; i < s.length; i++) {
    const o = e[s[i]];
    o && o.active() && n.push(o.wait());
  }
  return Promise.all(n);
}
function J0(e, t) {
  if (!t)
    return;
  let n = e.options;
  if (!n) {
    e.options = t;
    return;
  }
  return n.$shared && (e.options = n = Object.assign({}, n, {
    $shared: !1,
    $animations: {}
  })), n;
}
function ql(e, t) {
  const n = e && e.options || {}, s = n.reverse, i = n.min === void 0 ? t : 0, o = n.max === void 0 ? t : 0;
  return {
    start: s ? o : i,
    end: s ? i : o
  };
}
function Q0(e, t, n) {
  if (n === !1)
    return !1;
  const s = ql(e, n), i = ql(t, n);
  return {
    top: i.end,
    right: s.end,
    bottom: i.start,
    left: s.start
  };
}
function tb(e) {
  let t, n, s, i;
  return ot(e) ? (t = e.top, n = e.right, s = e.bottom, i = e.left) : t = n = s = i = e, {
    top: t,
    right: n,
    bottom: s,
    left: i,
    disabled: e === !1
  };
}
function Yu(e, t) {
  const n = [], s = e._getSortedDatasetMetas(t);
  let i, o;
  for (i = 0, o = s.length; i < o; ++i)
    n.push(s[i].index);
  return n;
}
function Xl(e, t, n, s = {}) {
  const i = e.keys, o = s.mode === "single";
  let r, a, l, c;
  if (t === null)
    return;
  let f = !1;
  for (r = 0, a = i.length; r < a; ++r) {
    if (l = +i[r], l === n) {
      if (f = !0, s.all)
        continue;
      break;
    }
    c = e.values[l], Rt(c) && (o || t === 0 || Pe(t) === Pe(c)) && (t += c);
  }
  return !f && !s.all ? 0 : t;
}
function eb(e, t) {
  const { iScale: n, vScale: s } = t, i = n.axis === "x" ? "x" : "y", o = s.axis === "x" ? "x" : "y", r = Object.keys(e), a = new Array(r.length);
  let l, c, f;
  for (l = 0, c = r.length; l < c; ++l)
    f = r[l], a[l] = {
      [i]: f,
      [o]: e[f]
    };
  return a;
}
function jo(e, t) {
  const n = e && e.options.stacked;
  return n || n === void 0 && t.stack !== void 0;
}
function nb(e, t, n) {
  return `${e.id}.${t.id}.${n.stack || n.type}`;
}
function sb(e) {
  const { min: t, max: n, minDefined: s, maxDefined: i } = e.getUserBounds();
  return {
    min: s ? t : Number.NEGATIVE_INFINITY,
    max: i ? n : Number.POSITIVE_INFINITY
  };
}
function ib(e, t, n) {
  const s = e[t] || (e[t] = {});
  return s[n] || (s[n] = {});
}
function Gl(e, t, n, s) {
  for (const i of t.getMatchingVisibleMetas(s).reverse()) {
    const o = e[i.index];
    if (n && o > 0 || !n && o < 0)
      return i.index;
  }
  return null;
}
function Zl(e, t) {
  const { chart: n, _cachedMeta: s } = e, i = n._stacks || (n._stacks = {}), { iScale: o, vScale: r, index: a } = s, l = o.axis, c = r.axis, f = nb(o, r, s), u = t.length;
  let h;
  for (let d = 0; d < u; ++d) {
    const p = t[d], { [l]: g, [c]: b } = p, y = p._stacks || (p._stacks = {});
    h = y[c] = ib(i, f, g), h[a] = b, h._top = Gl(h, r, !0, s.type), h._bottom = Gl(h, r, !1, s.type);
    const O = h._visualValues || (h._visualValues = {});
    O[a] = b;
  }
}
function zo(e, t) {
  const n = e.scales;
  return Object.keys(n).filter((s) => n[s].axis === t).shift();
}
function ob(e, t) {
  return Vn(e, {
    active: !1,
    dataset: void 0,
    datasetIndex: t,
    index: t,
    mode: "default",
    type: "dataset"
  });
}
function rb(e, t, n) {
  return Vn(e, {
    active: !1,
    dataIndex: t,
    parsed: void 0,
    raw: void 0,
    element: n,
    index: t,
    mode: "default",
    type: "data"
  });
}
function hs(e, t) {
  const n = e.controller.index, s = e.vScale && e.vScale.axis;
  if (s) {
    t = t || e._parsed;
    for (const i of t) {
      const o = i._stacks;
      if (!o || o[s] === void 0 || o[s][n] === void 0)
        return;
      delete o[s][n], o[s]._visualValues !== void 0 && o[s]._visualValues[n] !== void 0 && delete o[s]._visualValues[n];
    }
  }
}
const Ho = (e) => e === "reset" || e === "none", Jl = (e, t) => t ? e : Object.assign({}, e), ab = (e, t, n) => e && !t.hidden && t._stacked && {
  keys: Yu(n, !0),
  values: null
};
class Vs {
  constructor(t, n) {
    this.chart = t, this._ctx = t.ctx, this.index = n, this._cachedDataOpts = {}, this._cachedMeta = this.getMeta(), this._type = this._cachedMeta.type, this.options = void 0, this._parsing = !1, this._data = void 0, this._objectData = void 0, this._sharedOptions = void 0, this._drawStart = void 0, this._drawCount = void 0, this.enableOptionSharing = !1, this.supportsDecimation = !1, this.$context = void 0, this._syncList = [], this.datasetElementType = new.target.datasetElementType, this.dataElementType = new.target.dataElementType, this.initialize();
  }
  initialize() {
    const t = this._cachedMeta;
    this.configure(), this.linkScales(), t._stacked = jo(t.vScale, t), this.addElements(), this.options.fill && !this.chart.isPluginEnabled("filler") && console.warn("Tried to use the 'fill' option without the 'Filler' plugin enabled. Please import and register the 'Filler' plugin and make sure it is not disabled in the options");
  }
  updateIndex(t) {
    this.index !== t && hs(this._cachedMeta), this.index = t;
  }
  linkScales() {
    const t = this.chart, n = this._cachedMeta, s = this.getDataset(), i = (u, h, d, p) => u === "x" ? h : u === "r" ? p : d, o = n.xAxisID = ht(s.xAxisID, zo(t, "x")), r = n.yAxisID = ht(s.yAxisID, zo(t, "y")), a = n.rAxisID = ht(s.rAxisID, zo(t, "r")), l = n.indexAxis, c = n.iAxisID = i(l, o, r, a), f = n.vAxisID = i(l, r, o, a);
    n.xScale = this.getScaleForId(o), n.yScale = this.getScaleForId(r), n.rScale = this.getScaleForId(a), n.iScale = this.getScaleForId(c), n.vScale = this.getScaleForId(f);
  }
  getDataset() {
    return this.chart.data.datasets[this.index];
  }
  getMeta() {
    return this.chart.getDatasetMeta(this.index);
  }
  getScaleForId(t) {
    return this.chart.scales[t];
  }
  _getOtherScale(t) {
    const n = this._cachedMeta;
    return t === n.iScale ? n.vScale : n.iScale;
  }
  reset() {
    this._update("reset");
  }
  _destroy() {
    const t = this._cachedMeta;
    this._data && Pl(this._data, this), t._stacked && hs(t);
  }
  _dataCheck() {
    const t = this.getDataset(), n = t.data || (t.data = []), s = this._data;
    if (ot(n)) {
      const i = this._cachedMeta;
      this._data = eb(n, i);
    } else if (s !== n) {
      if (s) {
        Pl(s, this);
        const i = this._cachedMeta;
        hs(i), i._parsed = [];
      }
      n && Object.isExtensible(n) && Hm(n, this), this._syncList = [], this._data = n;
    }
  }
  addElements() {
    const t = this._cachedMeta;
    this._dataCheck(), this.datasetElementType && (t.dataset = new this.datasetElementType());
  }
  buildOrUpdateElements(t) {
    const n = this._cachedMeta, s = this.getDataset();
    let i = !1;
    this._dataCheck();
    const o = n._stacked;
    n._stacked = jo(n.vScale, n), n.stack !== s.stack && (i = !0, hs(n), n.stack = s.stack), this._resyncElements(t), (i || o !== n._stacked) && (Zl(this, n._parsed), n._stacked = jo(n.vScale, n));
  }
  configure() {
    const t = this.chart.config, n = t.datasetScopeKeys(this._type), s = t.getOptionScopes(this.getDataset(), n, !0);
    this.options = t.createResolver(s, this.getContext()), this._parsing = this.options.parsing, this._cachedDataOpts = {};
  }
  parse(t, n) {
    const { _cachedMeta: s, _data: i } = this, { iScale: o, _stacked: r } = s, a = o.axis;
    let l = t === 0 && n === i.length ? !0 : s._sorted, c = t > 0 && s._parsed[t - 1], f, u, h;
    if (this._parsing === !1)
      s._parsed = i, s._sorted = !0, h = i;
    else {
      Mt(i[t]) ? h = this.parseArrayData(s, i, t, n) : ot(i[t]) ? h = this.parseObjectData(s, i, t, n) : h = this.parsePrimitiveData(s, i, t, n);
      const d = () => u[a] === null || c && u[a] < c[a];
      for (f = 0; f < n; ++f)
        s._parsed[f + t] = u = h[f], l && (d() && (l = !1), c = u);
      s._sorted = l;
    }
    r && Zl(this, h);
  }
  parsePrimitiveData(t, n, s, i) {
    const { iScale: o, vScale: r } = t, a = o.axis, l = r.axis, c = o.getLabels(), f = o === r, u = new Array(i);
    let h, d, p;
    for (h = 0, d = i; h < d; ++h)
      p = h + s, u[h] = {
        [a]: f || o.parse(c[p], p),
        [l]: r.parse(n[p], p)
      };
    return u;
  }
  parseArrayData(t, n, s, i) {
    const { xScale: o, yScale: r } = t, a = new Array(i);
    let l, c, f, u;
    for (l = 0, c = i; l < c; ++l)
      f = l + s, u = n[f], a[l] = {
        x: o.parse(u[0], f),
        y: r.parse(u[1], f)
      };
    return a;
  }
  parseObjectData(t, n, s, i) {
    const { xScale: o, yScale: r } = t, { xAxisKey: a = "x", yAxisKey: l = "y" } = this._parsing, c = new Array(i);
    let f, u, h, d;
    for (f = 0, u = i; f < u; ++f)
      h = f + s, d = n[h], c[f] = {
        x: o.parse(Kn(d, a), h),
        y: r.parse(Kn(d, l), h)
      };
    return c;
  }
  getParsed(t) {
    return this._cachedMeta._parsed[t];
  }
  getDataElement(t) {
    return this._cachedMeta.data[t];
  }
  applyStack(t, n, s) {
    const i = this.chart, o = this._cachedMeta, r = n[t.axis], a = {
      keys: Yu(i, !0),
      values: n._stacks[t.axis]._visualValues
    };
    return Xl(a, r, o.index, {
      mode: s
    });
  }
  updateRangeFromParsed(t, n, s, i) {
    const o = s[n.axis];
    let r = o === null ? NaN : o;
    const a = i && s._stacks[n.axis];
    i && a && (i.values = a, r = Xl(i, o, this._cachedMeta.index)), t.min = Math.min(t.min, r), t.max = Math.max(t.max, r);
  }
  getMinMax(t, n) {
    const s = this._cachedMeta, i = s._parsed, o = s._sorted && t === s.iScale, r = i.length, a = this._getOtherScale(t), l = ab(n, s, this.chart), c = {
      min: Number.POSITIVE_INFINITY,
      max: Number.NEGATIVE_INFINITY
    }, { min: f, max: u } = sb(a);
    let h, d;
    function p() {
      d = i[h];
      const g = d[a.axis];
      return !Rt(d[t.axis]) || f > g || u < g;
    }
    for (h = 0; h < r && !(!p() && (this.updateRangeFromParsed(c, t, d, l), o)); ++h)
      ;
    if (o) {
      for (h = r - 1; h >= 0; --h)
        if (!p()) {
          this.updateRangeFromParsed(c, t, d, l);
          break;
        }
    }
    return c;
  }
  getAllParsedValues(t) {
    const n = this._cachedMeta._parsed, s = [];
    let i, o, r;
    for (i = 0, o = n.length; i < o; ++i)
      r = n[i][t.axis], Rt(r) && s.push(r);
    return s;
  }
  getMaxOverflow() {
    return !1;
  }
  getLabelAndValue(t) {
    const n = this._cachedMeta, s = n.iScale, i = n.vScale, o = this.getParsed(t);
    return {
      label: s ? "" + s.getLabelForValue(o[s.axis]) : "",
      value: i ? "" + i.getLabelForValue(o[i.axis]) : ""
    };
  }
  _update(t) {
    const n = this._cachedMeta;
    this.update(t || "default"), n._clip = tb(ht(this.options.clip, Q0(n.xScale, n.yScale, this.getMaxOverflow())));
  }
  update(t) {
  }
  draw() {
    const t = this._ctx, n = this.chart, s = this._cachedMeta, i = s.data || [], o = n.chartArea, r = [], a = this._drawStart || 0, l = this._drawCount || i.length - a, c = this.options.drawActiveElementsOnTop;
    let f;
    for (s.dataset && s.dataset.draw(t, o, a, l), f = a; f < a + l; ++f) {
      const u = i[f];
      u.hidden || (u.active && c ? r.push(u) : u.draw(t, o));
    }
    for (f = 0; f < r.length; ++f)
      r[f].draw(t, o);
  }
  getStyle(t, n) {
    const s = n ? "active" : "default";
    return t === void 0 && this._cachedMeta.dataset ? this.resolveDatasetElementOptions(s) : this.resolveDataElementOptions(t || 0, s);
  }
  getContext(t, n, s) {
    const i = this.getDataset();
    let o;
    if (t >= 0 && t < this._cachedMeta.data.length) {
      const r = this._cachedMeta.data[t];
      o = r.$context || (r.$context = rb(this.getContext(), t, r)), o.parsed = this.getParsed(t), o.raw = i.data[t], o.index = o.dataIndex = t;
    } else
      o = this.$context || (this.$context = ob(this.chart.getContext(), this.index)), o.dataset = i, o.index = o.datasetIndex = this.index;
    return o.active = !!n, o.mode = s, o;
  }
  resolveDatasetElementOptions(t) {
    return this._resolveElementOptions(this.datasetElementType.id, t);
  }
  resolveDataElementOptions(t, n) {
    return this._resolveElementOptions(this.dataElementType.id, n, t);
  }
  _resolveElementOptions(t, n = "default", s) {
    const i = n === "active", o = this._cachedDataOpts, r = t + "-" + n, a = o[r], l = this.enableOptionSharing && js(s);
    if (a)
      return Jl(a, l);
    const c = this.chart.config, f = c.datasetElementScopeKeys(this._type, t), u = i ? [
      `${t}Hover`,
      "hover",
      t,
      ""
    ] : [
      t,
      ""
    ], h = c.getOptionScopes(this.getDataset(), f), d = Object.keys(wt.elements[t]), p = () => this.getContext(s, i, n), g = c.resolveNamedOptions(h, d, p, u);
    return g.$shared && (g.$shared = l, o[r] = Object.freeze(Jl(g, l))), g;
  }
  _resolveAnimations(t, n, s) {
    const i = this.chart, o = this._cachedDataOpts, r = `animation-${n}`, a = o[r];
    if (a)
      return a;
    let l;
    if (i.options.animation !== !1) {
      const f = this.chart.config, u = f.datasetAnimationScopeKeys(this._type, n), h = f.getOptionScopes(this.getDataset(), u);
      l = f.createResolver(h, this.getContext(t, s, n));
    }
    const c = new Uu(i, l && l.animations);
    return l && l._cacheable && (o[r] = Object.freeze(c)), c;
  }
  getSharedOptions(t) {
    if (t.$shared)
      return this._sharedOptions || (this._sharedOptions = Object.assign({}, t));
  }
  includeOptions(t, n) {
    return !n || Ho(t) || this.chart._animationsDisabled;
  }
  _getSharedOptions(t, n) {
    const s = this.resolveDataElementOptions(t, n), i = this._sharedOptions, o = this.getSharedOptions(s), r = this.includeOptions(n, o) || o !== i;
    return this.updateSharedOptions(o, n, s), {
      sharedOptions: o,
      includeOptions: r
    };
  }
  updateElement(t, n, s, i) {
    Ho(i) ? Object.assign(t, s) : this._resolveAnimations(n, i).update(t, s);
  }
  updateSharedOptions(t, n, s) {
    t && !Ho(n) && this._resolveAnimations(void 0, n).update(t, s);
  }
  _setStyle(t, n, s, i) {
    t.active = i;
    const o = this.getStyle(n, i);
    this._resolveAnimations(n, s, i).update(t, {
      options: !i && this.getSharedOptions(o) || o
    });
  }
  removeHoverStyle(t, n, s) {
    this._setStyle(t, s, "active", !1);
  }
  setHoverStyle(t, n, s) {
    this._setStyle(t, s, "active", !0);
  }
  _removeDatasetHoverStyle() {
    const t = this._cachedMeta.dataset;
    t && this._setStyle(t, void 0, "active", !1);
  }
  _setDatasetHoverStyle() {
    const t = this._cachedMeta.dataset;
    t && this._setStyle(t, void 0, "active", !0);
  }
  _resyncElements(t) {
    const n = this._data, s = this._cachedMeta.data;
    for (const [a, l, c] of this._syncList)
      this[a](l, c);
    this._syncList = [];
    const i = s.length, o = n.length, r = Math.min(o, i);
    r && this.parse(0, r), o > i ? this._insertElements(i, o - i, t) : o < i && this._removeElements(o, i - o);
  }
  _insertElements(t, n, s = !0) {
    const i = this._cachedMeta, o = i.data, r = t + n;
    let a;
    const l = (c) => {
      for (c.length += n, a = c.length - 1; a >= r; a--)
        c[a] = c[a - n];
    };
    for (l(o), a = t; a < r; ++a)
      o[a] = new this.dataElementType();
    this._parsing && l(i._parsed), this.parse(t, n), s && this.updateElements(o, t, n, "reset");
  }
  updateElements(t, n, s, i) {
  }
  _removeElements(t, n) {
    const s = this._cachedMeta;
    if (this._parsing) {
      const i = s._parsed.splice(t, n);
      s._stacked && hs(s, i);
    }
    s.data.splice(t, n);
  }
  _sync(t) {
    if (this._parsing)
      this._syncList.push(t);
    else {
      const [n, s, i] = t;
      this[n](s, i);
    }
    this.chart._dataChanges.push([
      this.index,
      ...t
    ]);
  }
  _onDataPush() {
    const t = arguments.length;
    this._sync([
      "_insertElements",
      this.getDataset().data.length - t,
      t
    ]);
  }
  _onDataPop() {
    this._sync([
      "_removeElements",
      this._cachedMeta.data.length - 1,
      1
    ]);
  }
  _onDataShift() {
    this._sync([
      "_removeElements",
      0,
      1
    ]);
  }
  _onDataSplice(t, n) {
    n && this._sync([
      "_removeElements",
      t,
      n
    ]);
    const s = arguments.length - 2;
    s && this._sync([
      "_insertElements",
      t,
      s
    ]);
  }
  _onDataUnshift() {
    this._sync([
      "_insertElements",
      0,
      arguments.length
    ]);
  }
}
Z(Vs, "defaults", {}), Z(Vs, "datasetElementType", null), Z(Vs, "dataElementType", null);
function lb(e, t) {
  if (!e._cache.$bar) {
    const n = e.getMatchingVisibleMetas(t);
    let s = [];
    for (let i = 0, o = n.length; i < o; i++)
      s = s.concat(n[i].controller.getAllParsedValues(e));
    e._cache.$bar = Cu(s.sort((i, o) => i - o));
  }
  return e._cache.$bar;
}
function cb(e) {
  const t = e.iScale, n = lb(t, e.type);
  let s = t._length, i, o, r, a;
  const l = () => {
    r === 32767 || r === -32768 || (js(a) && (s = Math.min(s, Math.abs(r - a) || s)), a = r);
  };
  for (i = 0, o = n.length; i < o; ++i)
    r = t.getPixelForValue(n[i]), l();
  for (a = void 0, i = 0, o = t.ticks.length; i < o; ++i)
    r = t.getPixelForTick(i), l();
  return s;
}
function fb(e, t, n, s) {
  const i = n.barThickness;
  let o, r;
  return gt(i) ? (o = t.min * n.categoryPercentage, r = n.barPercentage) : (o = i * s, r = 1), {
    chunk: o / s,
    ratio: r,
    start: t.pixels[e] - o / 2
  };
}
function ub(e, t, n, s) {
  const i = t.pixels, o = i[e];
  let r = e > 0 ? i[e - 1] : null, a = e < i.length - 1 ? i[e + 1] : null;
  const l = n.categoryPercentage;
  r === null && (r = o - (a === null ? t.end - t.start : a - o)), a === null && (a = o + o - r);
  const c = o - (o - Math.min(r, a)) / 2 * l;
  return {
    chunk: Math.abs(a - r) / 2 * l / s,
    ratio: n.barPercentage,
    start: c
  };
}
function hb(e, t, n, s) {
  const i = n.parse(e[0], s), o = n.parse(e[1], s), r = Math.min(i, o), a = Math.max(i, o);
  let l = r, c = a;
  Math.abs(r) > Math.abs(a) && (l = a, c = r), t[n.axis] = c, t._custom = {
    barStart: l,
    barEnd: c,
    start: i,
    end: o,
    min: r,
    max: a
  };
}
function Ku(e, t, n, s) {
  return Mt(e) ? hb(e, t, n, s) : t[n.axis] = n.parse(e, s), t;
}
function Ql(e, t, n, s) {
  const i = e.iScale, o = e.vScale, r = i.getLabels(), a = i === o, l = [];
  let c, f, u, h;
  for (c = n, f = n + s; c < f; ++c)
    h = t[c], u = {}, u[i.axis] = a || i.parse(r[c], c), l.push(Ku(h, u, o, c));
  return l;
}
function Wo(e) {
  return e && e.barStart !== void 0 && e.barEnd !== void 0;
}
function db(e, t, n) {
  return e !== 0 ? Pe(e) : (t.isHorizontal() ? 1 : -1) * (t.min >= n ? 1 : -1);
}
function pb(e) {
  let t, n, s, i, o;
  return e.horizontal ? (t = e.base > e.x, n = "left", s = "right") : (t = e.base < e.y, n = "bottom", s = "top"), t ? (i = "end", o = "start") : (i = "start", o = "end"), {
    start: n,
    end: s,
    reverse: t,
    top: i,
    bottom: o
  };
}
function gb(e, t, n, s) {
  let i = t.borderSkipped;
  const o = {};
  if (!i) {
    e.borderSkipped = o;
    return;
  }
  if (i === !0) {
    e.borderSkipped = {
      top: !0,
      right: !0,
      bottom: !0,
      left: !0
    };
    return;
  }
  const { start: r, end: a, reverse: l, top: c, bottom: f } = pb(e);
  i === "middle" && n && (e.enableBorderRadius = !0, (n._top || 0) === s ? i = c : (n._bottom || 0) === s ? i = f : (o[tc(f, r, a, l)] = !0, i = c)), o[tc(i, r, a, l)] = !0, e.borderSkipped = o;
}
function tc(e, t, n, s) {
  return s ? (e = mb(e, t, n), e = ec(e, n, t)) : e = ec(e, t, n), e;
}
function mb(e, t, n) {
  return e === t ? n : e === n ? t : e;
}
function ec(e, t, n) {
  return e === "start" ? t : e === "end" ? n : e;
}
function bb(e, { inflateAmount: t }, n) {
  e.inflateAmount = t === "auto" ? n === 1 ? 0.33 : 0 : t;
}
class Pi extends Vs {
  parsePrimitiveData(t, n, s, i) {
    return Ql(t, n, s, i);
  }
  parseArrayData(t, n, s, i) {
    return Ql(t, n, s, i);
  }
  parseObjectData(t, n, s, i) {
    const { iScale: o, vScale: r } = t, { xAxisKey: a = "x", yAxisKey: l = "y" } = this._parsing, c = o.axis === "x" ? a : l, f = r.axis === "x" ? a : l, u = [];
    let h, d, p, g;
    for (h = s, d = s + i; h < d; ++h)
      g = n[h], p = {}, p[o.axis] = o.parse(Kn(g, c), h), u.push(Ku(Kn(g, f), p, r, h));
    return u;
  }
  updateRangeFromParsed(t, n, s, i) {
    super.updateRangeFromParsed(t, n, s, i);
    const o = s._custom;
    o && n === this._cachedMeta.vScale && (t.min = Math.min(t.min, o.min), t.max = Math.max(t.max, o.max));
  }
  getMaxOverflow() {
    return 0;
  }
  getLabelAndValue(t) {
    const n = this._cachedMeta, { iScale: s, vScale: i } = n, o = this.getParsed(t), r = o._custom, a = Wo(r) ? "[" + r.start + ", " + r.end + "]" : "" + i.getLabelForValue(o[i.axis]);
    return {
      label: "" + s.getLabelForValue(o[s.axis]),
      value: a
    };
  }
  initialize() {
    this.enableOptionSharing = !0, super.initialize();
    const t = this._cachedMeta;
    t.stack = this.getDataset().stack;
  }
  update(t) {
    const n = this._cachedMeta;
    this.updateElements(n.data, 0, n.data.length, t);
  }
  updateElements(t, n, s, i) {
    const o = i === "reset", { index: r, _cachedMeta: { vScale: a } } = this, l = a.getBasePixel(), c = a.isHorizontal(), f = this._getRuler(), { sharedOptions: u, includeOptions: h } = this._getSharedOptions(n, i);
    for (let d = n; d < n + s; d++) {
      const p = this.getParsed(d), g = o || gt(p[a.axis]) ? {
        base: l,
        head: l
      } : this._calculateBarValuePixels(d), b = this._calculateBarIndexPixels(d, f), y = (p._stacks || {})[a.axis], O = {
        horizontal: c,
        base: g.base,
        enableBorderRadius: !y || Wo(p._custom) || r === y._top || r === y._bottom,
        x: c ? g.head : b.center,
        y: c ? b.center : g.head,
        height: c ? b.size : Math.abs(g.size),
        width: c ? Math.abs(g.size) : b.size
      };
      h && (O.options = u || this.resolveDataElementOptions(d, t[d].active ? "active" : i));
      const M = O.options || t[d].options;
      gb(O, M, y, r), bb(O, M, f.ratio), this.updateElement(t[d], d, O, i);
    }
  }
  _getStacks(t, n) {
    const { iScale: s } = this._cachedMeta, i = s.getMatchingVisibleMetas(this._type).filter((f) => f.controller.options.grouped), o = s.options.stacked, r = [], a = this._cachedMeta.controller.getParsed(n), l = a && a[s.axis], c = (f) => {
      const u = f._parsed.find((d) => d[s.axis] === l), h = u && u[f.vScale.axis];
      if (gt(h) || isNaN(h))
        return !0;
    };
    for (const f of i)
      if (!(n !== void 0 && c(f)) && ((o === !1 || r.indexOf(f.stack) === -1 || o === void 0 && f.stack === void 0) && r.push(f.stack), f.index === t))
        break;
    return r.length || r.push(void 0), r;
  }
  _getStackCount(t) {
    return this._getStacks(void 0, t).length;
  }
  _getStackIndex(t, n, s) {
    const i = this._getStacks(t, s), o = n !== void 0 ? i.indexOf(n) : -1;
    return o === -1 ? i.length - 1 : o;
  }
  _getRuler() {
    const t = this.options, n = this._cachedMeta, s = n.iScale, i = [];
    let o, r;
    for (o = 0, r = n.data.length; o < r; ++o)
      i.push(s.getPixelForValue(this.getParsed(o)[s.axis], o));
    const a = t.barThickness;
    return {
      min: a || cb(n),
      pixels: i,
      start: s._startPixel,
      end: s._endPixel,
      stackCount: this._getStackCount(),
      scale: s,
      grouped: t.grouped,
      ratio: a ? 1 : t.categoryPercentage * t.barPercentage
    };
  }
  _calculateBarValuePixels(t) {
    const { _cachedMeta: { vScale: n, _stacked: s, index: i }, options: { base: o, minBarLength: r } } = this, a = o || 0, l = this.getParsed(t), c = l._custom, f = Wo(c);
    let u = l[n.axis], h = 0, d = s ? this.applyStack(n, l, s) : u, p, g;
    d !== u && (h = d - u, d = u), f && (u = c.barStart, d = c.barEnd - c.barStart, u !== 0 && Pe(u) !== Pe(c.barEnd) && (h = 0), h += u);
    const b = !gt(o) && !f ? o : h;
    let y = n.getPixelForValue(b);
    if (this.chart.getDataVisibility(t) ? p = n.getPixelForValue(h + d) : p = y, g = p - y, Math.abs(g) < r) {
      g = db(g, n, a) * r, u === a && (y -= g / 2);
      const O = n.getPixelForDecimal(0), M = n.getPixelForDecimal(1), P = Math.min(O, M), w = Math.max(O, M);
      y = Math.max(Math.min(y, w), P), p = y + g, s && !f && (l._stacks[n.axis]._visualValues[i] = n.getValueForPixel(p) - n.getValueForPixel(y));
    }
    if (y === n.getPixelForValue(a)) {
      const O = Pe(g) * n.getLineWidthForValue(a) / 2;
      y += O, g -= O;
    }
    return {
      size: g,
      base: y,
      head: p,
      center: p + g / 2
    };
  }
  _calculateBarIndexPixels(t, n) {
    const s = n.scale, i = this.options, o = i.skipNull, r = ht(i.maxBarThickness, 1 / 0);
    let a, l;
    if (n.grouped) {
      const c = o ? this._getStackCount(t) : n.stackCount, f = i.barThickness === "flex" ? ub(t, n, i, c) : fb(t, n, i, c), u = this._getStackIndex(this.index, this._cachedMeta.stack, o ? t : void 0);
      a = f.start + f.chunk * u + f.chunk / 2, l = Math.min(r, f.chunk * f.ratio);
    } else
      a = s.getPixelForValue(this.getParsed(t)[s.axis], t), l = Math.min(r, n.min * n.ratio);
    return {
      base: a - l / 2,
      head: a + l / 2,
      center: a,
      size: l
    };
  }
  draw() {
    const t = this._cachedMeta, n = t.vScale, s = t.data, i = s.length;
    let o = 0;
    for (; o < i; ++o)
      this.getParsed(o)[n.axis] !== null && !s[o].hidden && s[o].draw(this._ctx);
  }
}
Z(Pi, "id", "bar"), Z(Pi, "defaults", {
  datasetElementType: !1,
  dataElementType: "bar",
  categoryPercentage: 0.8,
  barPercentage: 0.9,
  grouped: !0,
  animations: {
    numbers: {
      type: "number",
      properties: [
        "x",
        "y",
        "base",
        "width",
        "height"
      ]
    }
  }
}), Z(Pi, "overrides", {
  scales: {
    _index_: {
      type: "category",
      offset: !0,
      grid: {
        offset: !0
      }
    },
    _value_: {
      type: "linear",
      beginAtZero: !0
    }
  }
});
function mn() {
  throw new Error("This method is not implemented: Check that a complete date adapter is provided.");
}
class va {
  constructor(t) {
    Z(this, "options");
    this.options = t || {};
  }
  /**
  * Override default date adapter methods.
  * Accepts type parameter to define options type.
  * @example
  * Chart._adapters._date.override<{myAdapterOption: string}>({
  *   init() {
  *     console.log(this.options.myAdapterOption);
  *   }
  * })
  */
  static override(t) {
    Object.assign(va.prototype, t);
  }
  // eslint-disable-next-line @typescript-eslint/no-empty-function
  init() {
  }
  formats() {
    return mn();
  }
  parse() {
    return mn();
  }
  format() {
    return mn();
  }
  add() {
    return mn();
  }
  diff() {
    return mn();
  }
  startOf() {
    return mn();
  }
  endOf() {
    return mn();
  }
}
var _b = {
  _date: va
};
function yb(e, t, n, s) {
  const { controller: i, data: o, _sorted: r } = e, a = i._cachedMeta.iScale;
  if (a && t === a.axis && t !== "r" && r && o.length) {
    const l = a._reversePixels ? jm : kr;
    if (s) {
      if (i._sharedOptions) {
        const c = o[0], f = typeof c.getRange == "function" && c.getRange(t);
        if (f) {
          const u = l(o, t, n - f), h = l(o, t, n + f);
          return {
            lo: u.lo,
            hi: h.hi
          };
        }
      }
    } else return l(o, t, n);
  }
  return {
    lo: 0,
    hi: o.length - 1
  };
}
function xo(e, t, n, s, i) {
  const o = e.getSortedVisibleDatasetMetas(), r = n[t];
  for (let a = 0, l = o.length; a < l; ++a) {
    const { index: c, data: f } = o[a], { lo: u, hi: h } = yb(o[a], t, r, i);
    for (let d = u; d <= h; ++d) {
      const p = f[d];
      p.skip || s(p, c, d);
    }
  }
}
function xb(e) {
  const t = e.indexOf("x") !== -1, n = e.indexOf("y") !== -1;
  return function(s, i) {
    const o = t ? Math.abs(s.x - i.x) : 0, r = n ? Math.abs(s.y - i.y) : 0;
    return Math.sqrt(Math.pow(o, 2) + Math.pow(r, 2));
  };
}
function Uo(e, t, n, s, i) {
  const o = [];
  return !i && !e.isPointInArea(t) || xo(e, n, t, function(a, l, c) {
    !i && !zs(a, e.chartArea, 0) || a.inRange(t.x, t.y, s) && o.push({
      element: a,
      datasetIndex: l,
      index: c
    });
  }, !0), o;
}
function vb(e, t, n, s) {
  let i = [];
  function o(r, a, l) {
    const { startAngle: c, endAngle: f } = r.getProps([
      "startAngle",
      "endAngle"
    ], s), { angle: u } = Fm(r, {
      x: t.x,
      y: t.y
    });
    Nu(u, c, f) && i.push({
      element: r,
      datasetIndex: a,
      index: l
    });
  }
  return xo(e, n, t, o), i;
}
function wb(e, t, n, s, i, o) {
  let r = [];
  const a = xb(n);
  let l = Number.POSITIVE_INFINITY;
  function c(f, u, h) {
    const d = f.inRange(t.x, t.y, i);
    if (s && !d)
      return;
    const p = f.getCenterPoint(i);
    if (!(!!o || e.isPointInArea(p)) && !d)
      return;
    const b = a(t, p);
    b < l ? (r = [
      {
        element: f,
        datasetIndex: u,
        index: h
      }
    ], l = b) : b === l && r.push({
      element: f,
      datasetIndex: u,
      index: h
    });
  }
  return xo(e, n, t, c), r;
}
function Yo(e, t, n, s, i, o) {
  return !o && !e.isPointInArea(t) ? [] : n === "r" && !s ? vb(e, t, n, i) : wb(e, t, n, s, i, o);
}
function nc(e, t, n, s, i) {
  const o = [], r = n === "x" ? "inXRange" : "inYRange";
  let a = !1;
  return xo(e, n, t, (l, c, f) => {
    l[r] && l[r](t[n], i) && (o.push({
      element: l,
      datasetIndex: c,
      index: f
    }), a = a || l.inRange(t.x, t.y, i));
  }), s && !a ? [] : o;
}
var Eb = {
  modes: {
    index(e, t, n, s) {
      const i = yn(t, e), o = n.axis || "x", r = n.includeInvisible || !1, a = n.intersect ? Uo(e, i, o, s, r) : Yo(e, i, o, !1, s, r), l = [];
      return a.length ? (e.getSortedVisibleDatasetMetas().forEach((c) => {
        const f = a[0].index, u = c.data[f];
        u && !u.skip && l.push({
          element: u,
          datasetIndex: c.index,
          index: f
        });
      }), l) : [];
    },
    dataset(e, t, n, s) {
      const i = yn(t, e), o = n.axis || "xy", r = n.includeInvisible || !1;
      let a = n.intersect ? Uo(e, i, o, s, r) : Yo(e, i, o, !1, s, r);
      if (a.length > 0) {
        const l = a[0].datasetIndex, c = e.getDatasetMeta(l).data;
        a = [];
        for (let f = 0; f < c.length; ++f)
          a.push({
            element: c[f],
            datasetIndex: l,
            index: f
          });
      }
      return a;
    },
    point(e, t, n, s) {
      const i = yn(t, e), o = n.axis || "xy", r = n.includeInvisible || !1;
      return Uo(e, i, o, s, r);
    },
    nearest(e, t, n, s) {
      const i = yn(t, e), o = n.axis || "xy", r = n.includeInvisible || !1;
      return Yo(e, i, o, n.intersect, s, r);
    },
    x(e, t, n, s) {
      const i = yn(t, e);
      return nc(e, i, "x", n.intersect, s);
    },
    y(e, t, n, s) {
      const i = yn(t, e);
      return nc(e, i, "y", n.intersect, s);
    }
  }
};
const qu = [
  "left",
  "top",
  "right",
  "bottom"
];
function ds(e, t) {
  return e.filter((n) => n.pos === t);
}
function sc(e, t) {
  return e.filter((n) => qu.indexOf(n.pos) === -1 && n.box.axis === t);
}
function ps(e, t) {
  return e.sort((n, s) => {
    const i = t ? s : n, o = t ? n : s;
    return i.weight === o.weight ? i.index - o.index : i.weight - o.weight;
  });
}
function Ob(e) {
  const t = [];
  let n, s, i, o, r, a;
  for (n = 0, s = (e || []).length; n < s; ++n)
    i = e[n], { position: o, options: { stack: r, stackWeight: a = 1 } } = i, t.push({
      index: n,
      box: i,
      pos: o,
      horizontal: i.isHorizontal(),
      weight: i.weight,
      stack: r && o + r,
      stackWeight: a
    });
  return t;
}
function Sb(e) {
  const t = {};
  for (const n of e) {
    const { stack: s, pos: i, stackWeight: o } = n;
    if (!s || !qu.includes(i))
      continue;
    const r = t[s] || (t[s] = {
      count: 0,
      placed: 0,
      weight: 0,
      size: 0
    });
    r.count++, r.weight += o;
  }
  return t;
}
function Mb(e, t) {
  const n = Sb(e), { vBoxMaxWidth: s, hBoxMaxHeight: i } = t;
  let o, r, a;
  for (o = 0, r = e.length; o < r; ++o) {
    a = e[o];
    const { fullSize: l } = a.box, c = n[a.stack], f = c && a.stackWeight / c.weight;
    a.horizontal ? (a.width = f ? f * s : l && t.availableWidth, a.height = i) : (a.width = s, a.height = f ? f * i : l && t.availableHeight);
  }
  return n;
}
function kb(e) {
  const t = Ob(e), n = ps(t.filter((c) => c.box.fullSize), !0), s = ps(ds(t, "left"), !0), i = ps(ds(t, "right")), o = ps(ds(t, "top"), !0), r = ps(ds(t, "bottom")), a = sc(t, "x"), l = sc(t, "y");
  return {
    fullSize: n,
    leftAndTop: s.concat(o),
    rightAndBottom: i.concat(l).concat(r).concat(a),
    chartArea: ds(t, "chartArea"),
    vertical: s.concat(i).concat(l),
    horizontal: o.concat(r).concat(a)
  };
}
function ic(e, t, n, s) {
  return Math.max(e[n], t[n]) + Math.max(e[s], t[s]);
}
function Xu(e, t) {
  e.top = Math.max(e.top, t.top), e.left = Math.max(e.left, t.left), e.bottom = Math.max(e.bottom, t.bottom), e.right = Math.max(e.right, t.right);
}
function Nb(e, t, n, s) {
  const { pos: i, box: o } = n, r = e.maxPadding;
  if (!ot(i)) {
    n.size && (e[i] -= n.size);
    const u = s[n.stack] || {
      size: 0,
      count: 1
    };
    u.size = Math.max(u.size, n.horizontal ? o.height : o.width), n.size = u.size / u.count, e[i] += n.size;
  }
  o.getPadding && Xu(r, o.getPadding());
  const a = Math.max(0, t.outerWidth - ic(r, e, "left", "right")), l = Math.max(0, t.outerHeight - ic(r, e, "top", "bottom")), c = a !== e.w, f = l !== e.h;
  return e.w = a, e.h = l, n.horizontal ? {
    same: c,
    other: f
  } : {
    same: f,
    other: c
  };
}
function Db(e) {
  const t = e.maxPadding;
  function n(s) {
    const i = Math.max(t[s] - e[s], 0);
    return e[s] += i, i;
  }
  e.y += n("top"), e.x += n("left"), n("right"), n("bottom");
}
function Cb(e, t) {
  const n = t.maxPadding;
  function s(i) {
    const o = {
      left: 0,
      top: 0,
      right: 0,
      bottom: 0
    };
    return i.forEach((r) => {
      o[r] = Math.max(t[r], n[r]);
    }), o;
  }
  return s(e ? [
    "left",
    "right"
  ] : [
    "top",
    "bottom"
  ]);
}
function vs(e, t, n, s) {
  const i = [];
  let o, r, a, l, c, f;
  for (o = 0, r = e.length, c = 0; o < r; ++o) {
    a = e[o], l = a.box, l.update(a.width || t.w, a.height || t.h, Cb(a.horizontal, t));
    const { same: u, other: h } = Nb(t, n, a, s);
    c |= u && i.length, f = f || h, l.fullSize || i.push(a);
  }
  return c && vs(i, t, n, s) || f;
}
function fi(e, t, n, s, i) {
  e.top = n, e.left = t, e.right = t + s, e.bottom = n + i, e.width = s, e.height = i;
}
function oc(e, t, n, s) {
  const i = n.padding;
  let { x: o, y: r } = t;
  for (const a of e) {
    const l = a.box, c = s[a.stack] || {
      placed: 0,
      weight: 1
    }, f = a.stackWeight / c.weight || 1;
    if (a.horizontal) {
      const u = t.w * f, h = c.size || l.height;
      js(c.start) && (r = c.start), l.fullSize ? fi(l, i.left, r, n.outerWidth - i.right - i.left, h) : fi(l, t.left + c.placed, r, u, h), c.start = r, c.placed += u, r = l.bottom;
    } else {
      const u = t.h * f, h = c.size || l.width;
      js(c.start) && (o = c.start), l.fullSize ? fi(l, o, i.top, h, n.outerHeight - i.bottom - i.top) : fi(l, o, t.top + c.placed, h, u), c.start = o, c.placed += u, o = l.right;
    }
  }
  t.x = o, t.y = r;
}
var ui = {
  addBox(e, t) {
    e.boxes || (e.boxes = []), t.fullSize = t.fullSize || !1, t.position = t.position || "top", t.weight = t.weight || 0, t._layers = t._layers || function() {
      return [
        {
          z: 0,
          draw(n) {
            t.draw(n);
          }
        }
      ];
    }, e.boxes.push(t);
  },
  removeBox(e, t) {
    const n = e.boxes ? e.boxes.indexOf(t) : -1;
    n !== -1 && e.boxes.splice(n, 1);
  },
  configure(e, t, n) {
    t.fullSize = n.fullSize, t.position = n.position, t.weight = n.weight;
  },
  update(e, t, n, s) {
    if (!e)
      return;
    const i = an(e.options.layout.padding), o = Math.max(t - i.width, 0), r = Math.max(n - i.height, 0), a = kb(e.boxes), l = a.vertical, c = a.horizontal;
    ft(e.boxes, (g) => {
      typeof g.beforeLayout == "function" && g.beforeLayout();
    });
    const f = l.reduce((g, b) => b.box.options && b.box.options.display === !1 ? g : g + 1, 0) || 1, u = Object.freeze({
      outerWidth: t,
      outerHeight: n,
      padding: i,
      availableWidth: o,
      availableHeight: r,
      vBoxMaxWidth: o / 2 / f,
      hBoxMaxHeight: r / 2
    }), h = Object.assign({}, i);
    Xu(h, an(s));
    const d = Object.assign({
      maxPadding: h,
      w: o,
      h: r,
      x: i.left,
      y: i.top
    }, i), p = Mb(l.concat(c), u);
    vs(a.fullSize, d, u, p), vs(l, d, u, p), vs(c, d, u, p) && vs(l, d, u, p), Db(d), oc(a.leftAndTop, d, u, p), d.x += d.w, d.y += d.h, oc(a.rightAndBottom, d, u, p), e.chartArea = {
      left: d.left,
      top: d.top,
      right: d.left + d.w,
      bottom: d.top + d.h,
      height: d.h,
      width: d.w
    }, ft(a.chartArea, (g) => {
      const b = g.box;
      Object.assign(b, e.chartArea), b.update(d.w, d.h, {
        left: 0,
        top: 0,
        right: 0,
        bottom: 0
      });
    });
  }
};
class Gu {
  acquireContext(t, n) {
  }
  releaseContext(t) {
    return !1;
  }
  addEventListener(t, n, s) {
  }
  removeEventListener(t, n, s) {
  }
  getDevicePixelRatio() {
    return 1;
  }
  getMaximumSize(t, n, s, i) {
    return n = Math.max(0, n || t.width), s = s || t.height, {
      width: n,
      height: Math.max(0, i ? Math.floor(n / i) : s)
    };
  }
  isAttached(t) {
    return !0;
  }
  updateConfig(t) {
  }
}
class Pb extends Gu {
  acquireContext(t) {
    return t && t.getContext && t.getContext("2d") || null;
  }
  updateConfig(t) {
    t.options.animation = !1;
  }
}
const Ti = "$chartjs", Tb = {
  touchstart: "mousedown",
  touchmove: "mousemove",
  touchend: "mouseup",
  pointerenter: "mouseenter",
  pointerdown: "mousedown",
  pointermove: "mousemove",
  pointerup: "mouseup",
  pointerleave: "mouseout",
  pointerout: "mouseout"
}, rc = (e) => e === null || e === "";
function Ab(e, t) {
  const n = e.style, s = e.getAttribute("height"), i = e.getAttribute("width");
  if (e[Ti] = {
    initial: {
      height: s,
      width: i,
      style: {
        display: n.display,
        height: n.height,
        width: n.width
      }
    }
  }, n.display = n.display || "block", n.boxSizing = n.boxSizing || "border-box", rc(i)) {
    const o = Hl(e, "width");
    o !== void 0 && (e.width = o);
  }
  if (rc(s))
    if (e.style.height === "")
      e.height = e.width / (t || 2);
    else {
      const o = Hl(e, "height");
      o !== void 0 && (e.height = o);
    }
  return e;
}
const Zu = R0 ? {
  passive: !0
} : !1;
function Vb(e, t, n) {
  e && e.addEventListener(t, n, Zu);
}
function Rb(e, t, n) {
  e && e.canvas && e.canvas.removeEventListener(t, n, Zu);
}
function Ib(e, t) {
  const n = Tb[e.type] || e.type, { x: s, y: i } = yn(e, t);
  return {
    type: n,
    chart: t,
    native: e,
    x: s !== void 0 ? s : null,
    y: i !== void 0 ? i : null
  };
}
function to(e, t) {
  for (const n of e)
    if (n === t || n.contains(t))
      return !0;
}
function Lb(e, t, n) {
  const s = e.canvas, i = new MutationObserver((o) => {
    let r = !1;
    for (const a of o)
      r = r || to(a.addedNodes, s), r = r && !to(a.removedNodes, s);
    r && n();
  });
  return i.observe(document, {
    childList: !0,
    subtree: !0
  }), i;
}
function Fb(e, t, n) {
  const s = e.canvas, i = new MutationObserver((o) => {
    let r = !1;
    for (const a of o)
      r = r || to(a.removedNodes, s), r = r && !to(a.addedNodes, s);
    r && n();
  });
  return i.observe(document, {
    childList: !0,
    subtree: !0
  }), i;
}
const Hs = /* @__PURE__ */ new Map();
let ac = 0;
function Ju() {
  const e = window.devicePixelRatio;
  e !== ac && (ac = e, Hs.forEach((t, n) => {
    n.currentDevicePixelRatio !== e && t();
  }));
}
function $b(e, t) {
  Hs.size || window.addEventListener("resize", Ju), Hs.set(e, t);
}
function Bb(e) {
  Hs.delete(e), Hs.size || window.removeEventListener("resize", Ju);
}
function jb(e, t, n) {
  const s = e.canvas, i = s && xa(s);
  if (!i)
    return;
  const o = Tu((a, l) => {
    const c = i.clientWidth;
    n(a, l), c < i.clientWidth && n();
  }, window), r = new ResizeObserver((a) => {
    const l = a[0], c = l.contentRect.width, f = l.contentRect.height;
    c === 0 && f === 0 || o(c, f);
  });
  return r.observe(i), $b(e, o), r;
}
function Ko(e, t, n) {
  n && n.disconnect(), t === "resize" && Bb(e);
}
function zb(e, t, n) {
  const s = e.canvas, i = Tu((o) => {
    e.ctx !== null && n(Ib(o, e));
  }, e);
  return Vb(s, t, i), i;
}
class Hb extends Gu {
  acquireContext(t, n) {
    const s = t && t.getContext && t.getContext("2d");
    return s && s.canvas === t ? (Ab(t, n), s) : null;
  }
  releaseContext(t) {
    const n = t.canvas;
    if (!n[Ti])
      return !1;
    const s = n[Ti].initial;
    [
      "height",
      "width"
    ].forEach((o) => {
      const r = s[o];
      gt(r) ? n.removeAttribute(o) : n.setAttribute(o, r);
    });
    const i = s.style || {};
    return Object.keys(i).forEach((o) => {
      n.style[o] = i[o];
    }), n.width = n.width, delete n[Ti], !0;
  }
  addEventListener(t, n, s) {
    this.removeEventListener(t, n);
    const i = t.$proxies || (t.$proxies = {}), r = {
      attach: Lb,
      detach: Fb,
      resize: jb
    }[n] || zb;
    i[n] = r(t, n, s);
  }
  removeEventListener(t, n) {
    const s = t.$proxies || (t.$proxies = {}), i = s[n];
    if (!i)
      return;
    ({
      attach: Ko,
      detach: Ko,
      resize: Ko
    }[n] || Rb)(t, n, i), s[n] = void 0;
  }
  getDevicePixelRatio() {
    return window.devicePixelRatio;
  }
  getMaximumSize(t, n, s, i) {
    return V0(t, n, s, i);
  }
  isAttached(t) {
    const n = t && xa(t);
    return !!(n && n.isConnected);
  }
}
function Wb(e) {
  return !ya() || typeof OffscreenCanvas < "u" && e instanceof OffscreenCanvas ? Pb : Hb;
}
var wi;
let Qn = (wi = class {
  constructor() {
    Z(this, "x");
    Z(this, "y");
    Z(this, "active", !1);
    Z(this, "options");
    Z(this, "$animations");
  }
  tooltipPosition(t) {
    const { x: n, y: s } = this.getProps([
      "x",
      "y"
    ], t);
    return {
      x: n,
      y: s
    };
  }
  hasValue() {
    return Zi(this.x) && Zi(this.y);
  }
  getProps(t, n) {
    const s = this.$animations;
    if (!n || !s)
      return this;
    const i = {};
    return t.forEach((o) => {
      i[o] = s[o] && s[o].active() ? s[o]._to : this[o];
    }), i;
  }
}, Z(wi, "defaults", {}), Z(wi, "defaultRoutes"), wi);
function Ub(e, t) {
  const n = e.options.ticks, s = Yb(e), i = Math.min(n.maxTicksLimit || s, s), o = n.major.enabled ? qb(t) : [], r = o.length, a = o[0], l = o[r - 1], c = [];
  if (r > i)
    return Xb(t, c, o, r / i), c;
  const f = Kb(o, t, i);
  if (r > 0) {
    let u, h;
    const d = r > 1 ? Math.round((l - a) / (r - 1)) : null;
    for (hi(t, c, f, gt(d) ? 0 : a - d, a), u = 0, h = r - 1; u < h; u++)
      hi(t, c, f, o[u], o[u + 1]);
    return hi(t, c, f, l, gt(d) ? t.length : l + d), c;
  }
  return hi(t, c, f), c;
}
function Yb(e) {
  const t = e.options.offset, n = e._tickSize(), s = e._length / n + (t ? 0 : 1), i = e._maxLength / n;
  return Math.floor(Math.min(s, i));
}
function Kb(e, t, n) {
  const s = Gb(e), i = t.length / n;
  if (!s)
    return Math.max(i, 1);
  const o = Vm(s);
  for (let r = 0, a = o.length - 1; r < a; r++) {
    const l = o[r];
    if (l > i)
      return l;
  }
  return Math.max(i, 1);
}
function qb(e) {
  const t = [];
  let n, s;
  for (n = 0, s = e.length; n < s; n++)
    e[n].major && t.push(n);
  return t;
}
function Xb(e, t, n, s) {
  let i = 0, o = n[0], r;
  for (s = Math.ceil(s), r = 0; r < e.length; r++)
    r === o && (t.push(e[r]), i++, o = n[i * s]);
}
function hi(e, t, n, s, i) {
  const o = ht(s, 0), r = Math.min(ht(i, e.length), e.length);
  let a = 0, l, c, f;
  for (n = Math.ceil(n), i && (l = i - s, n = l / Math.floor(l / n)), f = o; f < 0; )
    a++, f = Math.round(o + a * n);
  for (c = Math.max(o, 0); c < r; c++)
    c === f && (t.push(e[c]), a++, f = Math.round(o + a * n));
}
function Gb(e) {
  const t = e.length;
  let n, s;
  if (t < 2)
    return !1;
  for (s = e[0], n = 1; n < t; ++n)
    if (e[n] - e[n - 1] !== s)
      return !1;
  return s;
}
const Zb = (e) => e === "left" ? "right" : e === "right" ? "left" : e, lc = (e, t, n) => t === "top" || t === "left" ? e[t] + n : e[t] - n, cc = (e, t) => Math.min(t || e, e);
function fc(e, t) {
  const n = [], s = e.length / t, i = e.length;
  let o = 0;
  for (; o < i; o += s)
    n.push(e[Math.floor(o)]);
  return n;
}
function Jb(e, t, n) {
  const s = e.ticks.length, i = Math.min(t, s - 1), o = e._startPixel, r = e._endPixel, a = 1e-6;
  let l = e.getPixelForTick(i), c;
  if (!(n && (s === 1 ? c = Math.max(l - o, r - l) : t === 0 ? c = (e.getPixelForTick(1) - l) / 2 : c = (l - e.getPixelForTick(i - 1)) / 2, l += i < t ? c : -c, l < o - a || l > r + a)))
    return l;
}
function Qb(e, t) {
  ft(e, (n) => {
    const s = n.gc, i = s.length / 2;
    let o;
    if (i > t) {
      for (o = 0; o < i; ++o)
        delete n.data[s[o]];
      s.splice(0, i);
    }
  });
}
function gs(e) {
  return e.drawTicks ? e.tickLength : 0;
}
function uc(e, t) {
  if (!e.display)
    return 0;
  const n = Ne(e.font, t), s = an(e.padding);
  return (Mt(e.text) ? e.text.length : 1) * n.lineHeight + s.height;
}
function t_(e, t) {
  return Vn(e, {
    scale: t,
    type: "scale"
  });
}
function e_(e, t, n) {
  return Vn(e, {
    tick: n,
    index: t,
    type: "tick"
  });
}
function n_(e, t, n) {
  let s = Um(e);
  return (n && t !== "right" || !n && t === "right") && (s = Zb(s)), s;
}
function s_(e, t, n, s) {
  const { top: i, left: o, bottom: r, right: a, chart: l } = e, { chartArea: c, scales: f } = l;
  let u = 0, h, d, p;
  const g = r - i, b = a - o;
  if (e.isHorizontal()) {
    if (d = Tl(s, o, a), ot(n)) {
      const y = Object.keys(n)[0], O = n[y];
      p = f[y].getPixelForValue(O) + g - t;
    } else n === "center" ? p = (c.bottom + c.top) / 2 + g - t : p = lc(e, n, t);
    h = a - o;
  } else {
    if (ot(n)) {
      const y = Object.keys(n)[0], O = n[y];
      d = f[y].getPixelForValue(O) - b + t;
    } else n === "center" ? d = (c.left + c.right) / 2 - b + t : d = lc(e, n, t);
    p = Tl(s, r, i), u = n === "left" ? -ue : ue;
  }
  return {
    titleX: d,
    titleY: p,
    maxWidth: h,
    rotation: u
  };
}
class ts extends Qn {
  constructor(t) {
    super(), this.id = t.id, this.type = t.type, this.options = void 0, this.ctx = t.ctx, this.chart = t.chart, this.top = void 0, this.bottom = void 0, this.left = void 0, this.right = void 0, this.width = void 0, this.height = void 0, this._margins = {
      left: 0,
      right: 0,
      top: 0,
      bottom: 0
    }, this.maxWidth = void 0, this.maxHeight = void 0, this.paddingTop = void 0, this.paddingBottom = void 0, this.paddingLeft = void 0, this.paddingRight = void 0, this.axis = void 0, this.labelRotation = void 0, this.min = void 0, this.max = void 0, this._range = void 0, this.ticks = [], this._gridLineItems = null, this._labelItems = null, this._labelSizes = null, this._length = 0, this._maxLength = 0, this._longestTextCache = {}, this._startPixel = void 0, this._endPixel = void 0, this._reversePixels = !1, this._userMax = void 0, this._userMin = void 0, this._suggestedMax = void 0, this._suggestedMin = void 0, this._ticksLength = 0, this._borderValue = 0, this._cache = {}, this._dataLimitsCached = !1, this.$context = void 0;
  }
  init(t) {
    this.options = t.setContext(this.getContext()), this.axis = t.axis, this._userMin = this.parse(t.min), this._userMax = this.parse(t.max), this._suggestedMin = this.parse(t.suggestedMin), this._suggestedMax = this.parse(t.suggestedMax);
  }
  parse(t, n) {
    return t;
  }
  getUserBounds() {
    let { _userMin: t, _userMax: n, _suggestedMin: s, _suggestedMax: i } = this;
    return t = xe(t, Number.POSITIVE_INFINITY), n = xe(n, Number.NEGATIVE_INFINITY), s = xe(s, Number.POSITIVE_INFINITY), i = xe(i, Number.NEGATIVE_INFINITY), {
      min: xe(t, s),
      max: xe(n, i),
      minDefined: Rt(t),
      maxDefined: Rt(n)
    };
  }
  getMinMax(t) {
    let { min: n, max: s, minDefined: i, maxDefined: o } = this.getUserBounds(), r;
    if (i && o)
      return {
        min: n,
        max: s
      };
    const a = this.getMatchingVisibleMetas();
    for (let l = 0, c = a.length; l < c; ++l)
      r = a[l].controller.getMinMax(this, t), i || (n = Math.min(n, r.min)), o || (s = Math.max(s, r.max));
    return n = o && n > s ? s : n, s = i && n > s ? n : s, {
      min: xe(n, xe(s, n)),
      max: xe(s, xe(n, s))
    };
  }
  getPadding() {
    return {
      left: this.paddingLeft || 0,
      top: this.paddingTop || 0,
      right: this.paddingRight || 0,
      bottom: this.paddingBottom || 0
    };
  }
  getTicks() {
    return this.ticks;
  }
  getLabels() {
    const t = this.chart.data;
    return this.options.labels || (this.isHorizontal() ? t.xLabels : t.yLabels) || t.labels || [];
  }
  getLabelItems(t = this.chart.chartArea) {
    return this._labelItems || (this._labelItems = this._computeLabelItems(t));
  }
  beforeLayout() {
    this._cache = {}, this._dataLimitsCached = !1;
  }
  beforeUpdate() {
    yt(this.options.beforeUpdate, [
      this
    ]);
  }
  update(t, n, s) {
    const { beginAtZero: i, grace: o, ticks: r } = this.options, a = r.sampleSize;
    this.beforeUpdate(), this.maxWidth = t, this.maxHeight = n, this._margins = s = Object.assign({
      left: 0,
      right: 0,
      top: 0,
      bottom: 0
    }, s), this.ticks = null, this._labelSizes = null, this._gridLineItems = null, this._labelItems = null, this.beforeSetDimensions(), this.setDimensions(), this.afterSetDimensions(), this._maxLength = this.isHorizontal() ? this.width + s.left + s.right : this.height + s.top + s.bottom, this._dataLimitsCached || (this.beforeDataLimits(), this.determineDataLimits(), this.afterDataLimits(), this._range = h0(this, o, i), this._dataLimitsCached = !0), this.beforeBuildTicks(), this.ticks = this.buildTicks() || [], this.afterBuildTicks();
    const l = a < this.ticks.length;
    this._convertTicksToLabels(l ? fc(this.ticks, a) : this.ticks), this.configure(), this.beforeCalculateLabelRotation(), this.calculateLabelRotation(), this.afterCalculateLabelRotation(), r.display && (r.autoSkip || r.source === "auto") && (this.ticks = Ub(this, this.ticks), this._labelSizes = null, this.afterAutoSkip()), l && this._convertTicksToLabels(this.ticks), this.beforeFit(), this.fit(), this.afterFit(), this.afterUpdate();
  }
  configure() {
    let t = this.options.reverse, n, s;
    this.isHorizontal() ? (n = this.left, s = this.right) : (n = this.top, s = this.bottom, t = !t), this._startPixel = n, this._endPixel = s, this._reversePixels = t, this._length = s - n, this._alignToPixels = this.options.alignToPixels;
  }
  afterUpdate() {
    yt(this.options.afterUpdate, [
      this
    ]);
  }
  beforeSetDimensions() {
    yt(this.options.beforeSetDimensions, [
      this
    ]);
  }
  setDimensions() {
    this.isHorizontal() ? (this.width = this.maxWidth, this.left = 0, this.right = this.width) : (this.height = this.maxHeight, this.top = 0, this.bottom = this.height), this.paddingLeft = 0, this.paddingTop = 0, this.paddingRight = 0, this.paddingBottom = 0;
  }
  afterSetDimensions() {
    yt(this.options.afterSetDimensions, [
      this
    ]);
  }
  _callHooks(t) {
    this.chart.notifyPlugins(t, this.getContext()), yt(this.options[t], [
      this
    ]);
  }
  beforeDataLimits() {
    this._callHooks("beforeDataLimits");
  }
  determineDataLimits() {
  }
  afterDataLimits() {
    this._callHooks("afterDataLimits");
  }
  beforeBuildTicks() {
    this._callHooks("beforeBuildTicks");
  }
  buildTicks() {
    return [];
  }
  afterBuildTicks() {
    this._callHooks("afterBuildTicks");
  }
  beforeTickToLabelConversion() {
    yt(this.options.beforeTickToLabelConversion, [
      this
    ]);
  }
  generateTickLabels(t) {
    const n = this.options.ticks;
    let s, i, o;
    for (s = 0, i = t.length; s < i; s++)
      o = t[s], o.label = yt(n.callback, [
        o.value,
        s,
        t
      ], this);
  }
  afterTickToLabelConversion() {
    yt(this.options.afterTickToLabelConversion, [
      this
    ]);
  }
  beforeCalculateLabelRotation() {
    yt(this.options.beforeCalculateLabelRotation, [
      this
    ]);
  }
  calculateLabelRotation() {
    const t = this.options, n = t.ticks, s = cc(this.ticks.length, t.ticks.maxTicksLimit), i = n.minRotation || 0, o = n.maxRotation;
    let r = i, a, l, c;
    if (!this._isVisible() || !n.display || i >= o || s <= 1 || !this.isHorizontal()) {
      this.labelRotation = i;
      return;
    }
    const f = this._getLabelSizes(), u = f.widest.width, h = f.highest.height, d = he(this.chart.width - u, 0, this.maxWidth);
    a = t.offset ? this.maxWidth / s : d / (s - 1), u + 6 > a && (a = d / (s - (t.offset ? 0.5 : 1)), l = this.maxHeight - gs(t.grid) - n.padding - uc(t.title, this.chart.options.font), c = Math.sqrt(u * u + h * h), r = Lm(Math.min(Math.asin(he((f.highest.height + 6) / a, -1, 1)), Math.asin(he(l / c, -1, 1)) - Math.asin(he(h / c, -1, 1)))), r = Math.max(i, Math.min(o, r))), this.labelRotation = r;
  }
  afterCalculateLabelRotation() {
    yt(this.options.afterCalculateLabelRotation, [
      this
    ]);
  }
  afterAutoSkip() {
  }
  beforeFit() {
    yt(this.options.beforeFit, [
      this
    ]);
  }
  fit() {
    const t = {
      width: 0,
      height: 0
    }, { chart: n, options: { ticks: s, title: i, grid: o } } = this, r = this._isVisible(), a = this.isHorizontal();
    if (r) {
      const l = uc(i, n.options.font);
      if (a ? (t.width = this.maxWidth, t.height = gs(o) + l) : (t.height = this.maxHeight, t.width = gs(o) + l), s.display && this.ticks.length) {
        const { first: c, last: f, widest: u, highest: h } = this._getLabelSizes(), d = s.padding * 2, p = vn(this.labelRotation), g = Math.cos(p), b = Math.sin(p);
        if (a) {
          const y = s.mirror ? 0 : b * u.width + g * h.height;
          t.height = Math.min(this.maxHeight, t.height + y + d);
        } else {
          const y = s.mirror ? 0 : g * u.width + b * h.height;
          t.width = Math.min(this.maxWidth, t.width + y + d);
        }
        this._calculatePadding(c, f, b, g);
      }
    }
    this._handleMargins(), a ? (this.width = this._length = n.width - this._margins.left - this._margins.right, this.height = t.height) : (this.width = t.width, this.height = this._length = n.height - this._margins.top - this._margins.bottom);
  }
  _calculatePadding(t, n, s, i) {
    const { ticks: { align: o, padding: r }, position: a } = this.options, l = this.labelRotation !== 0, c = a !== "top" && this.axis === "x";
    if (this.isHorizontal()) {
      const f = this.getPixelForTick(0) - this.left, u = this.right - this.getPixelForTick(this.ticks.length - 1);
      let h = 0, d = 0;
      l ? c ? (h = i * t.width, d = s * n.height) : (h = s * t.height, d = i * n.width) : o === "start" ? d = n.width : o === "end" ? h = t.width : o !== "inner" && (h = t.width / 2, d = n.width / 2), this.paddingLeft = Math.max((h - f + r) * this.width / (this.width - f), 0), this.paddingRight = Math.max((d - u + r) * this.width / (this.width - u), 0);
    } else {
      let f = n.height / 2, u = t.height / 2;
      o === "start" ? (f = 0, u = t.height) : o === "end" && (f = n.height, u = 0), this.paddingTop = f + r, this.paddingBottom = u + r;
    }
  }
  _handleMargins() {
    this._margins && (this._margins.left = Math.max(this.paddingLeft, this._margins.left), this._margins.top = Math.max(this.paddingTop, this._margins.top), this._margins.right = Math.max(this.paddingRight, this._margins.right), this._margins.bottom = Math.max(this.paddingBottom, this._margins.bottom));
  }
  afterFit() {
    yt(this.options.afterFit, [
      this
    ]);
  }
  isHorizontal() {
    const { axis: t, position: n } = this.options;
    return n === "top" || n === "bottom" || t === "x";
  }
  isFullSize() {
    return this.options.fullSize;
  }
  _convertTicksToLabels(t) {
    this.beforeTickToLabelConversion(), this.generateTickLabels(t);
    let n, s;
    for (n = 0, s = t.length; n < s; n++)
      gt(t[n].label) && (t.splice(n, 1), s--, n--);
    this.afterTickToLabelConversion();
  }
  _getLabelSizes() {
    let t = this._labelSizes;
    if (!t) {
      const n = this.options.ticks.sampleSize;
      let s = this.ticks;
      n < s.length && (s = fc(s, n)), this._labelSizes = t = this._computeLabelSizes(s, s.length, this.options.ticks.maxTicksLimit);
    }
    return t;
  }
  _computeLabelSizes(t, n, s) {
    const { ctx: i, _longestTextCache: o } = this, r = [], a = [], l = Math.floor(n / cc(n, s));
    let c = 0, f = 0, u, h, d, p, g, b, y, O, M, P, w;
    for (u = 0; u < n; u += l) {
      if (p = t[u].label, g = this._resolveTickFontOptions(u), i.font = b = g.string, y = o[b] = o[b] || {
        data: {},
        gc: []
      }, O = g.lineHeight, M = P = 0, !gt(p) && !Mt(p))
        M = Ll(i, y.data, y.gc, M, p), P = O;
      else if (Mt(p))
        for (h = 0, d = p.length; h < d; ++h)
          w = p[h], !gt(w) && !Mt(w) && (M = Ll(i, y.data, y.gc, M, w), P += O);
      r.push(M), a.push(P), c = Math.max(M, c), f = Math.max(P, f);
    }
    Qb(o, n);
    const k = r.indexOf(c), v = a.indexOf(f), S = (D) => ({
      width: r[D] || 0,
      height: a[D] || 0
    });
    return {
      first: S(0),
      last: S(n - 1),
      widest: S(k),
      highest: S(v),
      widths: r,
      heights: a
    };
  }
  getLabelForValue(t) {
    return t;
  }
  getPixelForValue(t, n) {
    return NaN;
  }
  getValueForPixel(t) {
  }
  getPixelForTick(t) {
    const n = this.ticks;
    return t < 0 || t > n.length - 1 ? null : this.getPixelForValue(n[t].value);
  }
  getPixelForDecimal(t) {
    this._reversePixels && (t = 1 - t);
    const n = this._startPixel + t * this._length;
    return Bm(this._alignToPixels ? gn(this.chart, n, 0) : n);
  }
  getDecimalForPixel(t) {
    const n = (t - this._startPixel) / this._length;
    return this._reversePixels ? 1 - n : n;
  }
  getBasePixel() {
    return this.getPixelForValue(this.getBaseValue());
  }
  getBaseValue() {
    const { min: t, max: n } = this;
    return t < 0 && n < 0 ? n : t > 0 && n > 0 ? t : 0;
  }
  getContext(t) {
    const n = this.ticks || [];
    if (t >= 0 && t < n.length) {
      const s = n[t];
      return s.$context || (s.$context = e_(this.getContext(), t, s));
    }
    return this.$context || (this.$context = t_(this.chart.getContext(), this));
  }
  _tickSize() {
    const t = this.options.ticks, n = vn(this.labelRotation), s = Math.abs(Math.cos(n)), i = Math.abs(Math.sin(n)), o = this._getLabelSizes(), r = t.autoSkipPadding || 0, a = o ? o.widest.width + r : 0, l = o ? o.highest.height + r : 0;
    return this.isHorizontal() ? l * s > a * i ? a / s : l / i : l * i < a * s ? l / s : a / i;
  }
  _isVisible() {
    const t = this.options.display;
    return t !== "auto" ? !!t : this.getMatchingVisibleMetas().length > 0;
  }
  _computeGridLineItems(t) {
    const n = this.axis, s = this.chart, i = this.options, { grid: o, position: r, border: a } = i, l = o.offset, c = this.isHorizontal(), u = this.ticks.length + (l ? 1 : 0), h = gs(o), d = [], p = a.setContext(this.getContext()), g = p.display ? p.width : 0, b = g / 2, y = function(st) {
      return gn(s, st, g);
    };
    let O, M, P, w, k, v, S, D, F, z, j, tt;
    if (r === "top")
      O = y(this.bottom), v = this.bottom - h, D = O - b, z = y(t.top) + b, tt = t.bottom;
    else if (r === "bottom")
      O = y(this.top), z = t.top, tt = y(t.bottom) - b, v = O + b, D = this.top + h;
    else if (r === "left")
      O = y(this.right), k = this.right - h, S = O - b, F = y(t.left) + b, j = t.right;
    else if (r === "right")
      O = y(this.left), F = t.left, j = y(t.right) - b, k = O + b, S = this.left + h;
    else if (n === "x") {
      if (r === "center")
        O = y((t.top + t.bottom) / 2 + 0.5);
      else if (ot(r)) {
        const st = Object.keys(r)[0], W = r[st];
        O = y(this.chart.scales[st].getPixelForValue(W));
      }
      z = t.top, tt = t.bottom, v = O + b, D = v + h;
    } else if (n === "y") {
      if (r === "center")
        O = y((t.left + t.right) / 2);
      else if (ot(r)) {
        const st = Object.keys(r)[0], W = r[st];
        O = y(this.chart.scales[st].getPixelForValue(W));
      }
      k = O - b, S = k - h, F = t.left, j = t.right;
    }
    const Et = ht(i.ticks.maxTicksLimit, u), it = Math.max(1, Math.ceil(u / Et));
    for (M = 0; M < u; M += it) {
      const st = this.getContext(M), W = o.setContext(st), G = a.setContext(st), Ct = W.lineWidth, re = W.color, ee = G.dash || [], It = G.dashOffset, Nt = W.tickWidth, ae = W.tickColor, un = W.tickBorderDash || [], Re = W.tickBorderDashOffset;
      P = Jb(this, M, l), P !== void 0 && (w = gn(s, P, Ct), c ? k = S = F = j = w : v = D = z = tt = w, d.push({
        tx1: k,
        ty1: v,
        tx2: S,
        ty2: D,
        x1: F,
        y1: z,
        x2: j,
        y2: tt,
        width: Ct,
        color: re,
        borderDash: ee,
        borderDashOffset: It,
        tickWidth: Nt,
        tickColor: ae,
        tickBorderDash: un,
        tickBorderDashOffset: Re
      }));
    }
    return this._ticksLength = u, this._borderValue = O, d;
  }
  _computeLabelItems(t) {
    const n = this.axis, s = this.options, { position: i, ticks: o } = s, r = this.isHorizontal(), a = this.ticks, { align: l, crossAlign: c, padding: f, mirror: u } = o, h = gs(s.grid), d = h + f, p = u ? -f : d, g = -vn(this.labelRotation), b = [];
    let y, O, M, P, w, k, v, S, D, F, z, j, tt = "middle";
    if (i === "top")
      k = this.bottom - p, v = this._getXAxisLabelAlignment();
    else if (i === "bottom")
      k = this.top + p, v = this._getXAxisLabelAlignment();
    else if (i === "left") {
      const it = this._getYAxisLabelAlignment(h);
      v = it.textAlign, w = it.x;
    } else if (i === "right") {
      const it = this._getYAxisLabelAlignment(h);
      v = it.textAlign, w = it.x;
    } else if (n === "x") {
      if (i === "center")
        k = (t.top + t.bottom) / 2 + d;
      else if (ot(i)) {
        const it = Object.keys(i)[0], st = i[it];
        k = this.chart.scales[it].getPixelForValue(st) + d;
      }
      v = this._getXAxisLabelAlignment();
    } else if (n === "y") {
      if (i === "center")
        w = (t.left + t.right) / 2 - d;
      else if (ot(i)) {
        const it = Object.keys(i)[0], st = i[it];
        w = this.chart.scales[it].getPixelForValue(st);
      }
      v = this._getYAxisLabelAlignment(h).textAlign;
    }
    n === "y" && (l === "start" ? tt = "top" : l === "end" && (tt = "bottom"));
    const Et = this._getLabelSizes();
    for (y = 0, O = a.length; y < O; ++y) {
      M = a[y], P = M.label;
      const it = o.setContext(this.getContext(y));
      S = this.getPixelForTick(y) + o.labelOffset, D = this._resolveTickFontOptions(y), F = D.lineHeight, z = Mt(P) ? P.length : 1;
      const st = z / 2, W = it.color, G = it.textStrokeColor, Ct = it.textStrokeWidth;
      let re = v;
      r ? (w = S, v === "inner" && (y === O - 1 ? re = this.options.reverse ? "left" : "right" : y === 0 ? re = this.options.reverse ? "right" : "left" : re = "center"), i === "top" ? c === "near" || g !== 0 ? j = -z * F + F / 2 : c === "center" ? j = -Et.highest.height / 2 - st * F + F : j = -Et.highest.height + F / 2 : c === "near" || g !== 0 ? j = F / 2 : c === "center" ? j = Et.highest.height / 2 - st * F : j = Et.highest.height - z * F, u && (j *= -1), g !== 0 && !it.showLabelBackdrop && (w += F / 2 * Math.sin(g))) : (k = S, j = (1 - z) * F / 2);
      let ee;
      if (it.showLabelBackdrop) {
        const It = an(it.backdropPadding), Nt = Et.heights[y], ae = Et.widths[y];
        let un = j - It.top, Re = 0 - It.left;
        switch (tt) {
          case "middle":
            un -= Nt / 2;
            break;
          case "bottom":
            un -= Nt;
            break;
        }
        switch (v) {
          case "center":
            Re -= ae / 2;
            break;
          case "right":
            Re -= ae;
            break;
          case "inner":
            y === O - 1 ? Re -= ae : y > 0 && (Re -= ae / 2);
            break;
        }
        ee = {
          left: Re,
          top: un,
          width: ae + It.width,
          height: Nt + It.height,
          color: it.backdropColor
        };
      }
      b.push({
        label: P,
        font: D,
        textOffset: j,
        options: {
          rotation: g,
          color: W,
          strokeColor: G,
          strokeWidth: Ct,
          textAlign: re,
          textBaseline: tt,
          translation: [
            w,
            k
          ],
          backdrop: ee
        }
      });
    }
    return b;
  }
  _getXAxisLabelAlignment() {
    const { position: t, ticks: n } = this.options;
    if (-vn(this.labelRotation))
      return t === "top" ? "left" : "right";
    let i = "center";
    return n.align === "start" ? i = "left" : n.align === "end" ? i = "right" : n.align === "inner" && (i = "inner"), i;
  }
  _getYAxisLabelAlignment(t) {
    const { position: n, ticks: { crossAlign: s, mirror: i, padding: o } } = this.options, r = this._getLabelSizes(), a = t + o, l = r.widest.width;
    let c, f;
    return n === "left" ? i ? (f = this.right + o, s === "near" ? c = "left" : s === "center" ? (c = "center", f += l / 2) : (c = "right", f += l)) : (f = this.right - a, s === "near" ? c = "right" : s === "center" ? (c = "center", f -= l / 2) : (c = "left", f = this.left)) : n === "right" ? i ? (f = this.left + o, s === "near" ? c = "right" : s === "center" ? (c = "center", f -= l / 2) : (c = "left", f -= l)) : (f = this.left + a, s === "near" ? c = "left" : s === "center" ? (c = "center", f += l / 2) : (c = "right", f = this.right)) : c = "right", {
      textAlign: c,
      x: f
    };
  }
  _computeLabelArea() {
    if (this.options.ticks.mirror)
      return;
    const t = this.chart, n = this.options.position;
    if (n === "left" || n === "right")
      return {
        top: 0,
        left: this.left,
        bottom: t.height,
        right: this.right
      };
    if (n === "top" || n === "bottom")
      return {
        top: this.top,
        left: 0,
        bottom: this.bottom,
        right: t.width
      };
  }
  drawBackground() {
    const { ctx: t, options: { backgroundColor: n }, left: s, top: i, width: o, height: r } = this;
    n && (t.save(), t.fillStyle = n, t.fillRect(s, i, o, r), t.restore());
  }
  getLineWidthForValue(t) {
    const n = this.options.grid;
    if (!this._isVisible() || !n.display)
      return 0;
    const i = this.ticks.findIndex((o) => o.value === t);
    return i >= 0 ? n.setContext(this.getContext(i)).lineWidth : 0;
  }
  drawGrid(t) {
    const n = this.options.grid, s = this.ctx, i = this._gridLineItems || (this._gridLineItems = this._computeGridLineItems(t));
    let o, r;
    const a = (l, c, f) => {
      !f.width || !f.color || (s.save(), s.lineWidth = f.width, s.strokeStyle = f.color, s.setLineDash(f.borderDash || []), s.lineDashOffset = f.borderDashOffset, s.beginPath(), s.moveTo(l.x, l.y), s.lineTo(c.x, c.y), s.stroke(), s.restore());
    };
    if (n.display)
      for (o = 0, r = i.length; o < r; ++o) {
        const l = i[o];
        n.drawOnChartArea && a({
          x: l.x1,
          y: l.y1
        }, {
          x: l.x2,
          y: l.y2
        }, l), n.drawTicks && a({
          x: l.tx1,
          y: l.ty1
        }, {
          x: l.tx2,
          y: l.ty2
        }, {
          color: l.tickColor,
          width: l.tickWidth,
          borderDash: l.tickBorderDash,
          borderDashOffset: l.tickBorderDashOffset
        });
      }
  }
  drawBorder() {
    const { chart: t, ctx: n, options: { border: s, grid: i } } = this, o = s.setContext(this.getContext()), r = s.display ? o.width : 0;
    if (!r)
      return;
    const a = i.setContext(this.getContext(0)).lineWidth, l = this._borderValue;
    let c, f, u, h;
    this.isHorizontal() ? (c = gn(t, this.left, r) - r / 2, f = gn(t, this.right, a) + a / 2, u = h = l) : (u = gn(t, this.top, r) - r / 2, h = gn(t, this.bottom, a) + a / 2, c = f = l), n.save(), n.lineWidth = o.width, n.strokeStyle = o.color, n.beginPath(), n.moveTo(c, u), n.lineTo(f, h), n.stroke(), n.restore();
  }
  drawLabels(t) {
    if (!this.options.ticks.display)
      return;
    const s = this.ctx, i = this._computeLabelArea();
    i && pa(s, i);
    const o = this.getLabelItems(t);
    for (const r of o) {
      const a = r.options, l = r.font, c = r.label, f = r.textOffset;
      $l(s, c, 0, f, l, a);
    }
    i && ga(s);
  }
  drawTitle() {
    const { ctx: t, options: { position: n, title: s, reverse: i } } = this;
    if (!s.display)
      return;
    const o = Ne(s.font), r = an(s.padding), a = s.align;
    let l = o.lineHeight / 2;
    n === "bottom" || n === "center" || ot(n) ? (l += r.bottom, Mt(s.text) && (l += o.lineHeight * (s.text.length - 1))) : l += r.top;
    const { titleX: c, titleY: f, maxWidth: u, rotation: h } = s_(this, l, n, a);
    $l(t, s.text, 0, 0, o, {
      color: s.color,
      maxWidth: u,
      rotation: h,
      textAlign: n_(a, n, i),
      textBaseline: "middle",
      translation: [
        c,
        f
      ]
    });
  }
  draw(t) {
    this._isVisible() && (this.drawBackground(), this.drawGrid(t), this.drawBorder(), this.drawTitle(), this.drawLabels(t));
  }
  _layers() {
    const t = this.options, n = t.ticks && t.ticks.z || 0, s = ht(t.grid && t.grid.z, -1), i = ht(t.border && t.border.z, 0);
    return !this._isVisible() || this.draw !== ts.prototype.draw ? [
      {
        z: n,
        draw: (o) => {
          this.draw(o);
        }
      }
    ] : [
      {
        z: s,
        draw: (o) => {
          this.drawBackground(), this.drawGrid(o), this.drawTitle();
        }
      },
      {
        z: i,
        draw: () => {
          this.drawBorder();
        }
      },
      {
        z: n,
        draw: (o) => {
          this.drawLabels(o);
        }
      }
    ];
  }
  getMatchingVisibleMetas(t) {
    const n = this.chart.getSortedVisibleDatasetMetas(), s = this.axis + "AxisID", i = [];
    let o, r;
    for (o = 0, r = n.length; o < r; ++o) {
      const a = n[o];
      a[s] === this.id && (!t || a.type === t) && i.push(a);
    }
    return i;
  }
  _resolveTickFontOptions(t) {
    const n = this.options.ticks.setContext(this.getContext(t));
    return Ne(n.font);
  }
  _maxDigits() {
    const t = this._resolveTickFontOptions(0).lineHeight;
    return (this.isHorizontal() ? this.width : this.height) / t;
  }
}
class di {
  constructor(t, n, s) {
    this.type = t, this.scope = n, this.override = s, this.items = /* @__PURE__ */ Object.create(null);
  }
  isForType(t) {
    return Object.prototype.isPrototypeOf.call(this.type.prototype, t.prototype);
  }
  register(t) {
    const n = Object.getPrototypeOf(t);
    let s;
    r_(n) && (s = this.register(n));
    const i = this.items, o = t.id, r = this.scope + "." + o;
    if (!o)
      throw new Error("class does not have id: " + t);
    return o in i || (i[o] = t, i_(t, r, s), this.override && wt.override(t.id, t.overrides)), r;
  }
  get(t) {
    return this.items[t];
  }
  unregister(t) {
    const n = this.items, s = t.id, i = this.scope;
    s in n && delete n[s], i && s in wt[i] && (delete wt[i][s], this.override && delete An[s]);
  }
}
function i_(e, t, n) {
  const s = Bs(/* @__PURE__ */ Object.create(null), [
    n ? wt.get(n) : {},
    wt.get(t),
    e.defaults
  ]);
  wt.set(t, s), e.defaultRoutes && o_(t, e.defaultRoutes), e.descriptors && wt.describe(t, e.descriptors);
}
function o_(e, t) {
  Object.keys(t).forEach((n) => {
    const s = n.split("."), i = s.pop(), o = [
      e
    ].concat(s).join("."), r = t[n].split("."), a = r.pop(), l = r.join(".");
    wt.route(o, i, l, a);
  });
}
function r_(e) {
  return "id" in e && "defaults" in e;
}
class a_ {
  constructor() {
    this.controllers = new di(Vs, "datasets", !0), this.elements = new di(Qn, "elements"), this.plugins = new di(Object, "plugins"), this.scales = new di(ts, "scales"), this._typedRegistries = [
      this.controllers,
      this.scales,
      this.elements
    ];
  }
  add(...t) {
    this._each("register", t);
  }
  remove(...t) {
    this._each("unregister", t);
  }
  addControllers(...t) {
    this._each("register", t, this.controllers);
  }
  addElements(...t) {
    this._each("register", t, this.elements);
  }
  addPlugins(...t) {
    this._each("register", t, this.plugins);
  }
  addScales(...t) {
    this._each("register", t, this.scales);
  }
  getController(t) {
    return this._get(t, this.controllers, "controller");
  }
  getElement(t) {
    return this._get(t, this.elements, "element");
  }
  getPlugin(t) {
    return this._get(t, this.plugins, "plugin");
  }
  getScale(t) {
    return this._get(t, this.scales, "scale");
  }
  removeControllers(...t) {
    this._each("unregister", t, this.controllers);
  }
  removeElements(...t) {
    this._each("unregister", t, this.elements);
  }
  removePlugins(...t) {
    this._each("unregister", t, this.plugins);
  }
  removeScales(...t) {
    this._each("unregister", t, this.scales);
  }
  _each(t, n, s) {
    [
      ...n
    ].forEach((i) => {
      const o = s || this._getRegistryForType(i);
      s || o.isForType(i) || o === this.plugins && i.id ? this._exec(t, o, i) : ft(i, (r) => {
        const a = s || this._getRegistryForType(r);
        this._exec(t, a, r);
      });
    });
  }
  _exec(t, n, s) {
    const i = ua(t);
    yt(s["before" + i], [], s), n[t](s), yt(s["after" + i], [], s);
  }
  _getRegistryForType(t) {
    for (let n = 0; n < this._typedRegistries.length; n++) {
      const s = this._typedRegistries[n];
      if (s.isForType(t))
        return s;
    }
    return this.plugins;
  }
  _get(t, n, s) {
    const i = n.get(t);
    if (i === void 0)
      throw new Error('"' + t + '" is not a registered ' + s + ".");
    return i;
  }
}
var Ee = /* @__PURE__ */ new a_();
class l_ {
  constructor() {
    this._init = [];
  }
  notify(t, n, s, i) {
    n === "beforeInit" && (this._init = this._createDescriptors(t, !0), this._notify(this._init, t, "install"));
    const o = i ? this._descriptors(t).filter(i) : this._descriptors(t), r = this._notify(o, t, n, s);
    return n === "afterDestroy" && (this._notify(o, t, "stop"), this._notify(this._init, t, "uninstall")), r;
  }
  _notify(t, n, s, i) {
    i = i || {};
    for (const o of t) {
      const r = o.plugin, a = r[s], l = [
        n,
        i,
        o.options
      ];
      if (yt(a, l, r) === !1 && i.cancelable)
        return !1;
    }
    return !0;
  }
  invalidate() {
    gt(this._cache) || (this._oldCache = this._cache, this._cache = void 0);
  }
  _descriptors(t) {
    if (this._cache)
      return this._cache;
    const n = this._cache = this._createDescriptors(t);
    return this._notifyStateChanges(t), n;
  }
  _createDescriptors(t, n) {
    const s = t && t.config, i = ht(s.options && s.options.plugins, {}), o = c_(s);
    return i === !1 && !n ? [] : u_(t, o, i, n);
  }
  _notifyStateChanges(t) {
    const n = this._oldCache || [], s = this._cache, i = (o, r) => o.filter((a) => !r.some((l) => a.plugin.id === l.plugin.id));
    this._notify(i(n, s), t, "stop"), this._notify(i(s, n), t, "start");
  }
}
function c_(e) {
  const t = {}, n = [], s = Object.keys(Ee.plugins.items);
  for (let o = 0; o < s.length; o++)
    n.push(Ee.getPlugin(s[o]));
  const i = e.plugins || [];
  for (let o = 0; o < i.length; o++) {
    const r = i[o];
    n.indexOf(r) === -1 && (n.push(r), t[r.id] = !0);
  }
  return {
    plugins: n,
    localIds: t
  };
}
function f_(e, t) {
  return !t && e === !1 ? null : e === !0 ? {} : e;
}
function u_(e, { plugins: t, localIds: n }, s, i) {
  const o = [], r = e.getContext();
  for (const a of t) {
    const l = a.id, c = f_(s[l], i);
    c !== null && o.push({
      plugin: a,
      options: h_(e.config, {
        plugin: a,
        local: n[l]
      }, c, r)
    });
  }
  return o;
}
function h_(e, { plugin: t, local: n }, s, i) {
  const o = e.pluginScopeKeys(t), r = e.getOptionScopes(s, o);
  return n && t.defaults && r.push(t.defaults), e.createResolver(r, i, [
    ""
  ], {
    scriptable: !1,
    indexable: !1,
    allKeys: !0
  });
}
function Pr(e, t) {
  const n = wt.datasets[e] || {};
  return ((t.datasets || {})[e] || {}).indexAxis || t.indexAxis || n.indexAxis || "x";
}
function d_(e, t) {
  let n = e;
  return e === "_index_" ? n = t : e === "_value_" && (n = t === "x" ? "y" : "x"), n;
}
function p_(e, t) {
  return e === t ? "_index_" : "_value_";
}
function hc(e) {
  if (e === "x" || e === "y" || e === "r")
    return e;
}
function g_(e) {
  if (e === "top" || e === "bottom")
    return "x";
  if (e === "left" || e === "right")
    return "y";
}
function Tr(e, ...t) {
  if (hc(e))
    return e;
  for (const n of t) {
    const s = n.axis || g_(n.position) || e.length > 1 && hc(e[0].toLowerCase());
    if (s)
      return s;
  }
  throw new Error(`Cannot determine type of '${e}' axis. Please provide 'axis' or 'position' option.`);
}
function dc(e, t, n) {
  if (n[t + "AxisID"] === e)
    return {
      axis: t
    };
}
function m_(e, t) {
  if (t.data && t.data.datasets) {
    const n = t.data.datasets.filter((s) => s.xAxisID === e || s.yAxisID === e);
    if (n.length)
      return dc(e, "x", n[0]) || dc(e, "y", n[0]);
  }
  return {};
}
function b_(e, t) {
  const n = An[e.type] || {
    scales: {}
  }, s = t.scales || {}, i = Pr(e.type, t), o = /* @__PURE__ */ Object.create(null);
  return Object.keys(s).forEach((r) => {
    const a = s[r];
    if (!ot(a))
      return console.error(`Invalid scale configuration for scale: ${r}`);
    if (a._proxy)
      return console.warn(`Ignoring resolver passed as options for scale: ${r}`);
    const l = Tr(r, a, m_(r, e), wt.scales[a.type]), c = p_(l, i), f = n.scales || {};
    o[r] = Ds(/* @__PURE__ */ Object.create(null), [
      {
        axis: l
      },
      a,
      f[l],
      f[c]
    ]);
  }), e.data.datasets.forEach((r) => {
    const a = r.type || e.type, l = r.indexAxis || Pr(a, t), f = (An[a] || {}).scales || {};
    Object.keys(f).forEach((u) => {
      const h = d_(u, l), d = r[h + "AxisID"] || h;
      o[d] = o[d] || /* @__PURE__ */ Object.create(null), Ds(o[d], [
        {
          axis: h
        },
        s[d],
        f[u]
      ]);
    });
  }), Object.keys(o).forEach((r) => {
    const a = o[r];
    Ds(a, [
      wt.scales[a.type],
      wt.scale
    ]);
  }), o;
}
function Qu(e) {
  const t = e.options || (e.options = {});
  t.plugins = ht(t.plugins, {}), t.scales = b_(e, t);
}
function th(e) {
  return e = e || {}, e.datasets = e.datasets || [], e.labels = e.labels || [], e;
}
function __(e) {
  return e = e || {}, e.data = th(e.data), Qu(e), e;
}
const pc = /* @__PURE__ */ new Map(), eh = /* @__PURE__ */ new Set();
function pi(e, t) {
  let n = pc.get(e);
  return n || (n = t(), pc.set(e, n), eh.add(n)), n;
}
const ms = (e, t, n) => {
  const s = Kn(t, n);
  s !== void 0 && e.add(s);
};
class y_ {
  constructor(t) {
    this._config = __(t), this._scopeCache = /* @__PURE__ */ new Map(), this._resolverCache = /* @__PURE__ */ new Map();
  }
  get platform() {
    return this._config.platform;
  }
  get type() {
    return this._config.type;
  }
  set type(t) {
    this._config.type = t;
  }
  get data() {
    return this._config.data;
  }
  set data(t) {
    this._config.data = th(t);
  }
  get options() {
    return this._config.options;
  }
  set options(t) {
    this._config.options = t;
  }
  get plugins() {
    return this._config.plugins;
  }
  update() {
    const t = this._config;
    this.clearCache(), Qu(t);
  }
  clearCache() {
    this._scopeCache.clear(), this._resolverCache.clear();
  }
  datasetScopeKeys(t) {
    return pi(t, () => [
      [
        `datasets.${t}`,
        ""
      ]
    ]);
  }
  datasetAnimationScopeKeys(t, n) {
    return pi(`${t}.transition.${n}`, () => [
      [
        `datasets.${t}.transitions.${n}`,
        `transitions.${n}`
      ],
      [
        `datasets.${t}`,
        ""
      ]
    ]);
  }
  datasetElementScopeKeys(t, n) {
    return pi(`${t}-${n}`, () => [
      [
        `datasets.${t}.elements.${n}`,
        `datasets.${t}`,
        `elements.${n}`,
        ""
      ]
    ]);
  }
  pluginScopeKeys(t) {
    const n = t.id, s = this.type;
    return pi(`${s}-plugin-${n}`, () => [
      [
        `plugins.${n}`,
        ...t.additionalOptionScopes || []
      ]
    ]);
  }
  _cachedScopes(t, n) {
    const s = this._scopeCache;
    let i = s.get(t);
    return (!i || n) && (i = /* @__PURE__ */ new Map(), s.set(t, i)), i;
  }
  getOptionScopes(t, n, s) {
    const { options: i, type: o } = this, r = this._cachedScopes(t, s), a = r.get(n);
    if (a)
      return a;
    const l = /* @__PURE__ */ new Set();
    n.forEach((f) => {
      t && (l.add(t), f.forEach((u) => ms(l, t, u))), f.forEach((u) => ms(l, i, u)), f.forEach((u) => ms(l, An[o] || {}, u)), f.forEach((u) => ms(l, wt, u)), f.forEach((u) => ms(l, Nr, u));
    });
    const c = Array.from(l);
    return c.length === 0 && c.push(/* @__PURE__ */ Object.create(null)), eh.has(n) && r.set(n, c), c;
  }
  chartOptionScopes() {
    const { options: t, type: n } = this;
    return [
      t,
      An[n] || {},
      wt.datasets[n] || {},
      {
        type: n
      },
      wt,
      Nr
    ];
  }
  resolveNamedOptions(t, n, s, i = [
    ""
  ]) {
    const o = {
      $shared: !0
    }, { resolver: r, subPrefixes: a } = gc(this._resolverCache, t, i);
    let l = r;
    if (v_(r, n)) {
      o.$shared = !1, s = rn(s) ? s() : s;
      const c = this.createResolver(t, s, a);
      l = qn(r, s, c);
    }
    for (const c of n)
      o[c] = l[c];
    return o;
  }
  createResolver(t, n, s = [
    ""
  ], i) {
    const { resolver: o } = gc(this._resolverCache, t, s);
    return ot(n) ? qn(o, n, void 0, i) : o;
  }
}
function gc(e, t, n) {
  let s = e.get(t);
  s || (s = /* @__PURE__ */ new Map(), e.set(t, s));
  const i = n.join();
  let o = s.get(i);
  return o || (o = {
    resolver: ma(t, n),
    subPrefixes: n.filter((a) => !a.toLowerCase().includes("hover"))
  }, s.set(i, o)), o;
}
const x_ = (e) => ot(e) && Object.getOwnPropertyNames(e).some((t) => rn(e[t]));
function v_(e, t) {
  const { isScriptable: n, isIndexable: s } = Lu(e);
  for (const i of t) {
    const o = n(i), r = s(i), a = (r || o) && e[i];
    if (o && (rn(a) || x_(a)) || r && Mt(a))
      return !0;
  }
  return !1;
}
var w_ = "4.4.7";
const E_ = [
  "top",
  "bottom",
  "left",
  "right",
  "chartArea"
];
function mc(e, t) {
  return e === "top" || e === "bottom" || E_.indexOf(e) === -1 && t === "x";
}
function bc(e, t) {
  return function(n, s) {
    return n[e] === s[e] ? n[t] - s[t] : n[e] - s[e];
  };
}
function _c(e) {
  const t = e.chart, n = t.options.animation;
  t.notifyPlugins("afterRender"), yt(n && n.onComplete, [
    e
  ], t);
}
function O_(e) {
  const t = e.chart, n = t.options.animation;
  yt(n && n.onProgress, [
    e
  ], t);
}
function nh(e) {
  return ya() && typeof e == "string" ? e = document.getElementById(e) : e && e.length && (e = e[0]), e && e.canvas && (e = e.canvas), e;
}
const Ai = {}, yc = (e) => {
  const t = nh(e);
  return Object.values(Ai).filter((n) => n.canvas === t).pop();
};
function S_(e, t, n) {
  const s = Object.keys(e);
  for (const i of s) {
    const o = +i;
    if (o >= t) {
      const r = e[i];
      delete e[i], (n > 0 || o > t) && (e[o + n] = r);
    }
  }
}
function M_(e, t, n, s) {
  return !n || e.type === "mouseout" ? null : s ? t : e;
}
function gi(e, t, n) {
  return e.options.clip ? e[n] : t[n];
}
function k_(e, t) {
  const { xScale: n, yScale: s } = e;
  return n && s ? {
    left: gi(n, t, "left"),
    right: gi(n, t, "right"),
    top: gi(s, t, "top"),
    bottom: gi(s, t, "bottom")
  } : t;
}
class Pt {
  static register(...t) {
    Ee.add(...t), xc();
  }
  static unregister(...t) {
    Ee.remove(...t), xc();
  }
  constructor(t, n) {
    const s = this.config = new y_(n), i = nh(t), o = yc(i);
    if (o)
      throw new Error("Canvas is already in use. Chart with ID '" + o.id + "' must be destroyed before the canvas with ID '" + o.canvas.id + "' can be reused.");
    const r = s.createResolver(s.chartOptionScopes(), this.getContext());
    this.platform = new (s.platform || Wb(i))(), this.platform.updateConfig(s);
    const a = this.platform.acquireContext(i, r.aspectRatio), l = a && a.canvas, c = l && l.height, f = l && l.width;
    if (this.id = Sm(), this.ctx = a, this.canvas = l, this.width = f, this.height = c, this._options = r, this._aspectRatio = this.aspectRatio, this._layers = [], this._metasets = [], this._stacks = void 0, this.boxes = [], this.currentDevicePixelRatio = void 0, this.chartArea = void 0, this._active = [], this._lastEvent = void 0, this._listeners = {}, this._responsiveListeners = void 0, this._sortedMetasets = [], this.scales = {}, this._plugins = new l_(), this.$proxies = {}, this._hiddenIndices = {}, this.attached = !1, this._animationsDisabled = void 0, this.$context = void 0, this._doResize = Wm((u) => this.update(u), r.resizeDelay || 0), this._dataChanges = [], Ai[this.id] = this, !a || !l) {
      console.error("Failed to create chart: can't acquire context from the given item");
      return;
    }
    $e.listen(this, "complete", _c), $e.listen(this, "progress", O_), this._initialize(), this.attached && this.update();
  }
  get aspectRatio() {
    const { options: { aspectRatio: t, maintainAspectRatio: n }, width: s, height: i, _aspectRatio: o } = this;
    return gt(t) ? n && o ? o : i ? s / i : null : t;
  }
  get data() {
    return this.config.data;
  }
  set data(t) {
    this.config.data = t;
  }
  get options() {
    return this._options;
  }
  set options(t) {
    this.config.options = t;
  }
  get registry() {
    return Ee;
  }
  _initialize() {
    return this.notifyPlugins("beforeInit"), this.options.responsive ? this.resize() : zl(this, this.options.devicePixelRatio), this.bindEvents(), this.notifyPlugins("afterInit"), this;
  }
  clear() {
    return Fl(this.canvas, this.ctx), this;
  }
  stop() {
    return $e.stop(this), this;
  }
  resize(t, n) {
    $e.running(this) ? this._resizeBeforeDraw = {
      width: t,
      height: n
    } : this._resize(t, n);
  }
  _resize(t, n) {
    const s = this.options, i = this.canvas, o = s.maintainAspectRatio && this.aspectRatio, r = this.platform.getMaximumSize(i, t, n, o), a = s.devicePixelRatio || this.platform.getDevicePixelRatio(), l = this.width ? "resize" : "attach";
    this.width = r.width, this.height = r.height, this._aspectRatio = this.aspectRatio, zl(this, a, !0) && (this.notifyPlugins("resize", {
      size: r
    }), yt(s.onResize, [
      this,
      r
    ], this), this.attached && this._doResize(l) && this.render());
  }
  ensureScalesHaveIDs() {
    const n = this.options.scales || {};
    ft(n, (s, i) => {
      s.id = i;
    });
  }
  buildOrUpdateScales() {
    const t = this.options, n = t.scales, s = this.scales, i = Object.keys(s).reduce((r, a) => (r[a] = !1, r), {});
    let o = [];
    n && (o = o.concat(Object.keys(n).map((r) => {
      const a = n[r], l = Tr(r, a), c = l === "r", f = l === "x";
      return {
        options: a,
        dposition: c ? "chartArea" : f ? "bottom" : "left",
        dtype: c ? "radialLinear" : f ? "category" : "linear"
      };
    }))), ft(o, (r) => {
      const a = r.options, l = a.id, c = Tr(l, a), f = ht(a.type, r.dtype);
      (a.position === void 0 || mc(a.position, c) !== mc(r.dposition)) && (a.position = r.dposition), i[l] = !0;
      let u = null;
      if (l in s && s[l].type === f)
        u = s[l];
      else {
        const h = Ee.getScale(f);
        u = new h({
          id: l,
          type: f,
          ctx: this.ctx,
          chart: this
        }), s[u.id] = u;
      }
      u.init(a, t);
    }), ft(i, (r, a) => {
      r || delete s[a];
    }), ft(s, (r) => {
      ui.configure(this, r, r.options), ui.addBox(this, r);
    });
  }
  _updateMetasets() {
    const t = this._metasets, n = this.data.datasets.length, s = t.length;
    if (t.sort((i, o) => i.index - o.index), s > n) {
      for (let i = n; i < s; ++i)
        this._destroyDatasetMeta(i);
      t.splice(n, s - n);
    }
    this._sortedMetasets = t.slice(0).sort(bc("order", "index"));
  }
  _removeUnreferencedMetasets() {
    const { _metasets: t, data: { datasets: n } } = this;
    t.length > n.length && delete this._stacks, t.forEach((s, i) => {
      n.filter((o) => o === s._dataset).length === 0 && this._destroyDatasetMeta(i);
    });
  }
  buildOrUpdateControllers() {
    const t = [], n = this.data.datasets;
    let s, i;
    for (this._removeUnreferencedMetasets(), s = 0, i = n.length; s < i; s++) {
      const o = n[s];
      let r = this.getDatasetMeta(s);
      const a = o.type || this.config.type;
      if (r.type && r.type !== a && (this._destroyDatasetMeta(s), r = this.getDatasetMeta(s)), r.type = a, r.indexAxis = o.indexAxis || Pr(a, this.options), r.order = o.order || 0, r.index = s, r.label = "" + o.label, r.visible = this.isDatasetVisible(s), r.controller)
        r.controller.updateIndex(s), r.controller.linkScales();
      else {
        const l = Ee.getController(a), { datasetElementType: c, dataElementType: f } = wt.datasets[a];
        Object.assign(l, {
          dataElementType: Ee.getElement(f),
          datasetElementType: c && Ee.getElement(c)
        }), r.controller = new l(this, s), t.push(r.controller);
      }
    }
    return this._updateMetasets(), t;
  }
  _resetElements() {
    ft(this.data.datasets, (t, n) => {
      this.getDatasetMeta(n).controller.reset();
    }, this);
  }
  reset() {
    this._resetElements(), this.notifyPlugins("reset");
  }
  update(t) {
    const n = this.config;
    n.update();
    const s = this._options = n.createResolver(n.chartOptionScopes(), this.getContext()), i = this._animationsDisabled = !s.animation;
    if (this._updateScales(), this._checkEventBindings(), this._updateHiddenIndices(), this._plugins.invalidate(), this.notifyPlugins("beforeUpdate", {
      mode: t,
      cancelable: !0
    }) === !1)
      return;
    const o = this.buildOrUpdateControllers();
    this.notifyPlugins("beforeElementsUpdate");
    let r = 0;
    for (let c = 0, f = this.data.datasets.length; c < f; c++) {
      const { controller: u } = this.getDatasetMeta(c), h = !i && o.indexOf(u) === -1;
      u.buildOrUpdateElements(h), r = Math.max(+u.getMaxOverflow(), r);
    }
    r = this._minPadding = s.layout.autoPadding ? r : 0, this._updateLayout(r), i || ft(o, (c) => {
      c.reset();
    }), this._updateDatasets(t), this.notifyPlugins("afterUpdate", {
      mode: t
    }), this._layers.sort(bc("z", "_idx"));
    const { _active: a, _lastEvent: l } = this;
    l ? this._eventHandler(l, !0) : a.length && this._updateHoverStyles(a, a, !0), this.render();
  }
  _updateScales() {
    ft(this.scales, (t) => {
      ui.removeBox(this, t);
    }), this.ensureScalesHaveIDs(), this.buildOrUpdateScales();
  }
  _checkEventBindings() {
    const t = this.options, n = new Set(Object.keys(this._listeners)), s = new Set(t.events);
    (!kl(n, s) || !!this._responsiveListeners !== t.responsive) && (this.unbindEvents(), this.bindEvents());
  }
  _updateHiddenIndices() {
    const { _hiddenIndices: t } = this, n = this._getUniformDataChanges() || [];
    for (const { method: s, start: i, count: o } of n) {
      const r = s === "_removeElements" ? -o : o;
      S_(t, i, r);
    }
  }
  _getUniformDataChanges() {
    const t = this._dataChanges;
    if (!t || !t.length)
      return;
    this._dataChanges = [];
    const n = this.data.datasets.length, s = (o) => new Set(t.filter((r) => r[0] === o).map((r, a) => a + "," + r.splice(1).join(","))), i = s(0);
    for (let o = 1; o < n; o++)
      if (!kl(i, s(o)))
        return;
    return Array.from(i).map((o) => o.split(",")).map((o) => ({
      method: o[1],
      start: +o[2],
      count: +o[3]
    }));
  }
  _updateLayout(t) {
    if (this.notifyPlugins("beforeLayout", {
      cancelable: !0
    }) === !1)
      return;
    ui.update(this, this.width, this.height, t);
    const n = this.chartArea, s = n.width <= 0 || n.height <= 0;
    this._layers = [], ft(this.boxes, (i) => {
      s && i.position === "chartArea" || (i.configure && i.configure(), this._layers.push(...i._layers()));
    }, this), this._layers.forEach((i, o) => {
      i._idx = o;
    }), this.notifyPlugins("afterLayout");
  }
  _updateDatasets(t) {
    if (this.notifyPlugins("beforeDatasetsUpdate", {
      mode: t,
      cancelable: !0
    }) !== !1) {
      for (let n = 0, s = this.data.datasets.length; n < s; ++n)
        this.getDatasetMeta(n).controller.configure();
      for (let n = 0, s = this.data.datasets.length; n < s; ++n)
        this._updateDataset(n, rn(t) ? t({
          datasetIndex: n
        }) : t);
      this.notifyPlugins("afterDatasetsUpdate", {
        mode: t
      });
    }
  }
  _updateDataset(t, n) {
    const s = this.getDatasetMeta(t), i = {
      meta: s,
      index: t,
      mode: n,
      cancelable: !0
    };
    this.notifyPlugins("beforeDatasetUpdate", i) !== !1 && (s.controller._update(n), i.cancelable = !1, this.notifyPlugins("afterDatasetUpdate", i));
  }
  render() {
    this.notifyPlugins("beforeRender", {
      cancelable: !0
    }) !== !1 && ($e.has(this) ? this.attached && !$e.running(this) && $e.start(this) : (this.draw(), _c({
      chart: this
    })));
  }
  draw() {
    let t;
    if (this._resizeBeforeDraw) {
      const { width: s, height: i } = this._resizeBeforeDraw;
      this._resizeBeforeDraw = null, this._resize(s, i);
    }
    if (this.clear(), this.width <= 0 || this.height <= 0 || this.notifyPlugins("beforeDraw", {
      cancelable: !0
    }) === !1)
      return;
    const n = this._layers;
    for (t = 0; t < n.length && n[t].z <= 0; ++t)
      n[t].draw(this.chartArea);
    for (this._drawDatasets(); t < n.length; ++t)
      n[t].draw(this.chartArea);
    this.notifyPlugins("afterDraw");
  }
  _getSortedDatasetMetas(t) {
    const n = this._sortedMetasets, s = [];
    let i, o;
    for (i = 0, o = n.length; i < o; ++i) {
      const r = n[i];
      (!t || r.visible) && s.push(r);
    }
    return s;
  }
  getSortedVisibleDatasetMetas() {
    return this._getSortedDatasetMetas(!0);
  }
  _drawDatasets() {
    if (this.notifyPlugins("beforeDatasetsDraw", {
      cancelable: !0
    }) === !1)
      return;
    const t = this.getSortedVisibleDatasetMetas();
    for (let n = t.length - 1; n >= 0; --n)
      this._drawDataset(t[n]);
    this.notifyPlugins("afterDatasetsDraw");
  }
  _drawDataset(t) {
    const n = this.ctx, s = t._clip, i = !s.disabled, o = k_(t, this.chartArea), r = {
      meta: t,
      index: t.index,
      cancelable: !0
    };
    this.notifyPlugins("beforeDatasetDraw", r) !== !1 && (i && pa(n, {
      left: s.left === !1 ? 0 : o.left - s.left,
      right: s.right === !1 ? this.width : o.right + s.right,
      top: s.top === !1 ? 0 : o.top - s.top,
      bottom: s.bottom === !1 ? this.height : o.bottom + s.bottom
    }), t.controller.draw(), i && ga(n), r.cancelable = !1, this.notifyPlugins("afterDatasetDraw", r));
  }
  isPointInArea(t) {
    return zs(t, this.chartArea, this._minPadding);
  }
  getElementsAtEventForMode(t, n, s, i) {
    const o = Eb.modes[n];
    return typeof o == "function" ? o(this, t, s, i) : [];
  }
  getDatasetMeta(t) {
    const n = this.data.datasets[t], s = this._metasets;
    let i = s.filter((o) => o && o._dataset === n).pop();
    return i || (i = {
      type: null,
      data: [],
      dataset: null,
      controller: null,
      hidden: null,
      xAxisID: null,
      yAxisID: null,
      order: n && n.order || 0,
      index: t,
      _dataset: n,
      _parsed: [],
      _sorted: !1
    }, s.push(i)), i;
  }
  getContext() {
    return this.$context || (this.$context = Vn(null, {
      chart: this,
      type: "chart"
    }));
  }
  getVisibleDatasetCount() {
    return this.getSortedVisibleDatasetMetas().length;
  }
  isDatasetVisible(t) {
    const n = this.data.datasets[t];
    if (!n)
      return !1;
    const s = this.getDatasetMeta(t);
    return typeof s.hidden == "boolean" ? !s.hidden : !n.hidden;
  }
  setDatasetVisibility(t, n) {
    const s = this.getDatasetMeta(t);
    s.hidden = !n;
  }
  toggleDataVisibility(t) {
    this._hiddenIndices[t] = !this._hiddenIndices[t];
  }
  getDataVisibility(t) {
    return !this._hiddenIndices[t];
  }
  _updateVisibility(t, n, s) {
    const i = s ? "show" : "hide", o = this.getDatasetMeta(t), r = o.controller._resolveAnimations(void 0, i);
    js(n) ? (o.data[n].hidden = !s, this.update()) : (this.setDatasetVisibility(t, s), r.update(o, {
      visible: s
    }), this.update((a) => a.datasetIndex === t ? i : void 0));
  }
  hide(t, n) {
    this._updateVisibility(t, n, !1);
  }
  show(t, n) {
    this._updateVisibility(t, n, !0);
  }
  _destroyDatasetMeta(t) {
    const n = this._metasets[t];
    n && n.controller && n.controller._destroy(), delete this._metasets[t];
  }
  _stop() {
    let t, n;
    for (this.stop(), $e.remove(this), t = 0, n = this.data.datasets.length; t < n; ++t)
      this._destroyDatasetMeta(t);
  }
  destroy() {
    this.notifyPlugins("beforeDestroy");
    const { canvas: t, ctx: n } = this;
    this._stop(), this.config.clearCache(), t && (this.unbindEvents(), Fl(t, n), this.platform.releaseContext(n), this.canvas = null, this.ctx = null), delete Ai[this.id], this.notifyPlugins("afterDestroy");
  }
  toBase64Image(...t) {
    return this.canvas.toDataURL(...t);
  }
  bindEvents() {
    this.bindUserEvents(), this.options.responsive ? this.bindResponsiveEvents() : this.attached = !0;
  }
  bindUserEvents() {
    const t = this._listeners, n = this.platform, s = (o, r) => {
      n.addEventListener(this, o, r), t[o] = r;
    }, i = (o, r, a) => {
      o.offsetX = r, o.offsetY = a, this._eventHandler(o);
    };
    ft(this.options.events, (o) => s(o, i));
  }
  bindResponsiveEvents() {
    this._responsiveListeners || (this._responsiveListeners = {});
    const t = this._responsiveListeners, n = this.platform, s = (l, c) => {
      n.addEventListener(this, l, c), t[l] = c;
    }, i = (l, c) => {
      t[l] && (n.removeEventListener(this, l, c), delete t[l]);
    }, o = (l, c) => {
      this.canvas && this.resize(l, c);
    };
    let r;
    const a = () => {
      i("attach", a), this.attached = !0, this.resize(), s("resize", o), s("detach", r);
    };
    r = () => {
      this.attached = !1, i("resize", o), this._stop(), this._resize(0, 0), s("attach", a);
    }, n.isAttached(this.canvas) ? a() : r();
  }
  unbindEvents() {
    ft(this._listeners, (t, n) => {
      this.platform.removeEventListener(this, n, t);
    }), this._listeners = {}, ft(this._responsiveListeners, (t, n) => {
      this.platform.removeEventListener(this, n, t);
    }), this._responsiveListeners = void 0;
  }
  updateHoverStyle(t, n, s) {
    const i = s ? "set" : "remove";
    let o, r, a, l;
    for (n === "dataset" && (o = this.getDatasetMeta(t[0].datasetIndex), o.controller["_" + i + "DatasetHoverStyle"]()), a = 0, l = t.length; a < l; ++a) {
      r = t[a];
      const c = r && this.getDatasetMeta(r.datasetIndex).controller;
      c && c[i + "HoverStyle"](r.element, r.datasetIndex, r.index);
    }
  }
  getActiveElements() {
    return this._active || [];
  }
  setActiveElements(t) {
    const n = this._active || [], s = t.map(({ datasetIndex: o, index: r }) => {
      const a = this.getDatasetMeta(o);
      if (!a)
        throw new Error("No dataset found at index " + o);
      return {
        datasetIndex: o,
        element: a.data[r],
        index: r
      };
    });
    !qi(s, n) && (this._active = s, this._lastEvent = null, this._updateHoverStyles(s, n));
  }
  notifyPlugins(t, n, s) {
    return this._plugins.notify(this, t, n, s);
  }
  isPluginEnabled(t) {
    return this._plugins._cache.filter((n) => n.plugin.id === t).length === 1;
  }
  _updateHoverStyles(t, n, s) {
    const i = this.options.hover, o = (l, c) => l.filter((f) => !c.some((u) => f.datasetIndex === u.datasetIndex && f.index === u.index)), r = o(n, t), a = s ? t : o(t, n);
    r.length && this.updateHoverStyle(r, i.mode, !1), a.length && i.mode && this.updateHoverStyle(a, i.mode, !0);
  }
  _eventHandler(t, n) {
    const s = {
      event: t,
      replay: n,
      cancelable: !0,
      inChartArea: this.isPointInArea(t)
    }, i = (r) => (r.options.events || this.options.events).includes(t.native.type);
    if (this.notifyPlugins("beforeEvent", s, i) === !1)
      return;
    const o = this._handleEvent(t, n, s.inChartArea);
    return s.cancelable = !1, this.notifyPlugins("afterEvent", s, i), (o || s.changed) && this.render(), this;
  }
  _handleEvent(t, n, s) {
    const { _active: i = [], options: o } = this, r = n, a = this._getActiveElements(t, i, s, r), l = Pm(t), c = M_(t, this._lastEvent, s, l);
    s && (this._lastEvent = null, yt(o.onHover, [
      t,
      a,
      this
    ], this), l && yt(o.onClick, [
      t,
      a,
      this
    ], this));
    const f = !qi(a, i);
    return (f || n) && (this._active = a, this._updateHoverStyles(a, i, n)), this._lastEvent = c, f;
  }
  _getActiveElements(t, n, s, i) {
    if (t.type === "mouseout")
      return [];
    if (!s)
      return n;
    const o = this.options.hover;
    return this.getElementsAtEventForMode(t, o.mode, o, i);
  }
}
Z(Pt, "defaults", wt), Z(Pt, "instances", Ai), Z(Pt, "overrides", An), Z(Pt, "registry", Ee), Z(Pt, "version", w_), Z(Pt, "getChart", yc);
function xc() {
  return ft(Pt.instances, (e) => e._plugins.invalidate());
}
function sh(e, t, n = t) {
  e.lineCap = ht(n.borderCapStyle, t.borderCapStyle), e.setLineDash(ht(n.borderDash, t.borderDash)), e.lineDashOffset = ht(n.borderDashOffset, t.borderDashOffset), e.lineJoin = ht(n.borderJoinStyle, t.borderJoinStyle), e.lineWidth = ht(n.borderWidth, t.borderWidth), e.strokeStyle = ht(n.borderColor, t.borderColor);
}
function N_(e, t, n) {
  e.lineTo(n.x, n.y);
}
function D_(e) {
  return e.stepped ? s0 : e.tension || e.cubicInterpolationMode === "monotone" ? i0 : N_;
}
function ih(e, t, n = {}) {
  const s = e.length, { start: i = 0, end: o = s - 1 } = n, { start: r, end: a } = t, l = Math.max(i, r), c = Math.min(o, a), f = i < r && o < r || i > a && o > a;
  return {
    count: s,
    start: l,
    loop: t.loop,
    ilen: c < l && !f ? s + c - l : c - l
  };
}
function C_(e, t, n, s) {
  const { points: i, options: o } = t, { count: r, start: a, loop: l, ilen: c } = ih(i, n, s), f = D_(o);
  let { move: u = !0, reverse: h } = s || {}, d, p, g;
  for (d = 0; d <= c; ++d)
    p = i[(a + (h ? c - d : d)) % r], !p.skip && (u ? (e.moveTo(p.x, p.y), u = !1) : f(e, g, p, h, o.stepped), g = p);
  return l && (p = i[(a + (h ? c : 0)) % r], f(e, g, p, h, o.stepped)), !!l;
}
function P_(e, t, n, s) {
  const i = t.points, { count: o, start: r, ilen: a } = ih(i, n, s), { move: l = !0, reverse: c } = s || {};
  let f = 0, u = 0, h, d, p, g, b, y;
  const O = (P) => (r + (c ? a - P : P)) % o, M = () => {
    g !== b && (e.lineTo(f, b), e.lineTo(f, g), e.lineTo(f, y));
  };
  for (l && (d = i[O(0)], e.moveTo(d.x, d.y)), h = 0; h <= a; ++h) {
    if (d = i[O(h)], d.skip)
      continue;
    const P = d.x, w = d.y, k = P | 0;
    k === p ? (w < g ? g = w : w > b && (b = w), f = (u * f + P) / ++u) : (M(), e.lineTo(P, w), p = k, u = 0, g = b = w), y = w;
  }
  M();
}
function Ar(e) {
  const t = e.options, n = t.borderDash && t.borderDash.length;
  return !e._decimated && !e._loop && !t.tension && t.cubicInterpolationMode !== "monotone" && !t.stepped && !n ? P_ : C_;
}
function T_(e) {
  return e.stepped ? I0 : e.tension || e.cubicInterpolationMode === "monotone" ? L0 : xn;
}
function A_(e, t, n, s) {
  let i = t._path;
  i || (i = t._path = new Path2D(), t.path(i, n, s) && i.closePath()), sh(e, t.options), e.stroke(i);
}
function V_(e, t, n, s) {
  const { segments: i, options: o } = t, r = Ar(t);
  for (const a of i)
    sh(e, o, a.style), e.beginPath(), r(e, t, a, {
      start: n,
      end: n + s - 1
    }) && e.closePath(), e.stroke();
}
const R_ = typeof Path2D == "function";
function I_(e, t, n, s) {
  R_ && !t.options.segment ? A_(e, t, n, s) : V_(e, t, n, s);
}
class wn extends Qn {
  constructor(t) {
    super(), this.animated = !0, this.options = void 0, this._chart = void 0, this._loop = void 0, this._fullLoop = void 0, this._path = void 0, this._points = void 0, this._segments = void 0, this._decimated = !1, this._pointsUpdated = !1, this._datasetIndex = void 0, t && Object.assign(this, t);
  }
  updateControlPoints(t, n) {
    const s = this.options;
    if ((s.tension || s.cubicInterpolationMode === "monotone") && !s.stepped && !this._pointsUpdated) {
      const i = s.spanGaps ? this._loop : this._fullLoop;
      N0(this._points, s, t, i, n), this._pointsUpdated = !0;
    }
  }
  set points(t) {
    this._points = t, delete this._segments, delete this._path, this._pointsUpdated = !1;
  }
  get points() {
    return this._points;
  }
  get segments() {
    return this._segments || (this._segments = U0(this, this.options.segment));
  }
  first() {
    const t = this.segments, n = this.points;
    return t.length && n[t[0].start];
  }
  last() {
    const t = this.segments, n = this.points, s = t.length;
    return s && n[t[s - 1].end];
  }
  interpolate(t, n) {
    const s = this.options, i = t[n], o = this.points, r = Wu(this, {
      property: n,
      start: i,
      end: i
    });
    if (!r.length)
      return;
    const a = [], l = T_(s);
    let c, f;
    for (c = 0, f = r.length; c < f; ++c) {
      const { start: u, end: h } = r[c], d = o[u], p = o[h];
      if (d === p) {
        a.push(d);
        continue;
      }
      const g = Math.abs((i - d[n]) / (p[n] - d[n])), b = l(d, p, g, s.stepped);
      b[n] = t[n], a.push(b);
    }
    return a.length === 1 ? a[0] : a;
  }
  pathSegment(t, n, s) {
    return Ar(this)(t, this, n, s);
  }
  path(t, n, s) {
    const i = this.segments, o = Ar(this);
    let r = this._loop;
    n = n || 0, s = s || this.points.length - n;
    for (const a of i)
      r &= o(t, this, a, {
        start: n,
        end: n + s - 1
      });
    return !!r;
  }
  draw(t, n, s, i) {
    const o = this.options || {};
    (this.points || []).length && o.borderWidth && (t.save(), I_(t, this, s, i), t.restore()), this.animated && (this._pointsUpdated = !1, this._path = void 0);
  }
}
Z(wn, "id", "line"), Z(wn, "defaults", {
  borderCapStyle: "butt",
  borderDash: [],
  borderDashOffset: 0,
  borderJoinStyle: "miter",
  borderWidth: 3,
  capBezierPoints: !0,
  cubicInterpolationMode: "default",
  fill: !1,
  spanGaps: !1,
  stepped: !1,
  tension: 0
}), Z(wn, "defaultRoutes", {
  backgroundColor: "backgroundColor",
  borderColor: "borderColor"
}), Z(wn, "descriptors", {
  _scriptable: !0,
  _indexable: (t) => t !== "borderDash" && t !== "fill"
});
function vc(e, t, n, s) {
  const i = e.options, { [n]: o } = e.getProps([
    n
  ], s);
  return Math.abs(t - o) < i.radius + i.hitRadius;
}
class Vi extends Qn {
  constructor(n) {
    super();
    Z(this, "parsed");
    Z(this, "skip");
    Z(this, "stop");
    this.options = void 0, this.parsed = void 0, this.skip = void 0, this.stop = void 0, n && Object.assign(this, n);
  }
  inRange(n, s, i) {
    const o = this.options, { x: r, y: a } = this.getProps([
      "x",
      "y"
    ], i);
    return Math.pow(n - r, 2) + Math.pow(s - a, 2) < Math.pow(o.hitRadius + o.radius, 2);
  }
  inXRange(n, s) {
    return vc(this, n, "x", s);
  }
  inYRange(n, s) {
    return vc(this, n, "y", s);
  }
  getCenterPoint(n) {
    const { x: s, y: i } = this.getProps([
      "x",
      "y"
    ], n);
    return {
      x: s,
      y: i
    };
  }
  size(n) {
    n = n || this.options || {};
    let s = n.radius || 0;
    s = Math.max(s, s && n.hoverRadius || 0);
    const i = s && n.borderWidth || 0;
    return (s + i) * 2;
  }
  draw(n, s) {
    const i = this.options;
    this.skip || i.radius < 0.1 || !zs(this, s, this.size(i) / 2) || (n.strokeStyle = i.borderColor, n.lineWidth = i.borderWidth, n.fillStyle = i.backgroundColor, Dr(n, i, this.x, this.y));
  }
  getRange() {
    const n = this.options || {};
    return n.radius + n.hitRadius;
  }
}
Z(Vi, "id", "point"), /**
* @type {any}
*/
Z(Vi, "defaults", {
  borderWidth: 1,
  hitRadius: 1,
  hoverBorderWidth: 1,
  hoverRadius: 4,
  pointStyle: "circle",
  radius: 3,
  rotation: 0
}), /**
* @type {any}
*/
Z(Vi, "defaultRoutes", {
  backgroundColor: "backgroundColor",
  borderColor: "borderColor"
});
function oh(e, t) {
  const { x: n, y: s, base: i, width: o, height: r } = e.getProps([
    "x",
    "y",
    "base",
    "width",
    "height"
  ], t);
  let a, l, c, f, u;
  return e.horizontal ? (u = r / 2, a = Math.min(n, i), l = Math.max(n, i), c = s - u, f = s + u) : (u = o / 2, a = n - u, l = n + u, c = Math.min(s, i), f = Math.max(s, i)), {
    left: a,
    top: c,
    right: l,
    bottom: f
  };
}
function en(e, t, n, s) {
  return e ? 0 : he(t, n, s);
}
function L_(e, t, n) {
  const s = e.options.borderWidth, i = e.borderSkipped, o = Iu(s);
  return {
    t: en(i.top, o.top, 0, n),
    r: en(i.right, o.right, 0, t),
    b: en(i.bottom, o.bottom, 0, n),
    l: en(i.left, o.left, 0, t)
  };
}
function F_(e, t, n) {
  const { enableBorderRadius: s } = e.getProps([
    "enableBorderRadius"
  ]), i = e.options.borderRadius, o = As(i), r = Math.min(t, n), a = e.borderSkipped, l = s || ot(i);
  return {
    topLeft: en(!l || a.top || a.left, o.topLeft, 0, r),
    topRight: en(!l || a.top || a.right, o.topRight, 0, r),
    bottomLeft: en(!l || a.bottom || a.left, o.bottomLeft, 0, r),
    bottomRight: en(!l || a.bottom || a.right, o.bottomRight, 0, r)
  };
}
function $_(e) {
  const t = oh(e), n = t.right - t.left, s = t.bottom - t.top, i = L_(e, n / 2, s / 2), o = F_(e, n / 2, s / 2);
  return {
    outer: {
      x: t.left,
      y: t.top,
      w: n,
      h: s,
      radius: o
    },
    inner: {
      x: t.left + i.l,
      y: t.top + i.t,
      w: n - i.l - i.r,
      h: s - i.t - i.b,
      radius: {
        topLeft: Math.max(0, o.topLeft - Math.max(i.t, i.l)),
        topRight: Math.max(0, o.topRight - Math.max(i.t, i.r)),
        bottomLeft: Math.max(0, o.bottomLeft - Math.max(i.b, i.l)),
        bottomRight: Math.max(0, o.bottomRight - Math.max(i.b, i.r))
      }
    }
  };
}
function qo(e, t, n, s) {
  const i = t === null, o = n === null, a = e && !(i && o) && oh(e, s);
  return a && (i || Ji(t, a.left, a.right)) && (o || Ji(n, a.top, a.bottom));
}
function B_(e) {
  return e.topLeft || e.topRight || e.bottomLeft || e.bottomRight;
}
function j_(e, t) {
  e.rect(t.x, t.y, t.w, t.h);
}
function Xo(e, t, n = {}) {
  const s = e.x !== n.x ? -t : 0, i = e.y !== n.y ? -t : 0, o = (e.x + e.w !== n.x + n.w ? t : 0) - s, r = (e.y + e.h !== n.y + n.h ? t : 0) - i;
  return {
    x: e.x + s,
    y: e.y + i,
    w: e.w + o,
    h: e.h + r,
    radius: e.radius
  };
}
class Ri extends Qn {
  constructor(t) {
    super(), this.options = void 0, this.horizontal = void 0, this.base = void 0, this.width = void 0, this.height = void 0, this.inflateAmount = void 0, t && Object.assign(this, t);
  }
  draw(t) {
    const { inflateAmount: n, options: { borderColor: s, backgroundColor: i } } = this, { inner: o, outer: r } = $_(this), a = B_(r.radius) ? Cr : j_;
    t.save(), (r.w !== o.w || r.h !== o.h) && (t.beginPath(), a(t, Xo(r, n, o)), t.clip(), a(t, Xo(o, -n, r)), t.fillStyle = s, t.fill("evenodd")), t.beginPath(), a(t, Xo(o, n)), t.fillStyle = i, t.fill(), t.restore();
  }
  inRange(t, n, s) {
    return qo(this, t, n, s);
  }
  inXRange(t, n) {
    return qo(this, t, null, n);
  }
  inYRange(t, n) {
    return qo(this, null, t, n);
  }
  getCenterPoint(t) {
    const { x: n, y: s, base: i, horizontal: o } = this.getProps([
      "x",
      "y",
      "base",
      "horizontal"
    ], t);
    return {
      x: o ? (n + i) / 2 : n,
      y: o ? s : (s + i) / 2
    };
  }
  getRange(t) {
    return t === "x" ? this.width / 2 : this.height / 2;
  }
}
Z(Ri, "id", "bar"), Z(Ri, "defaults", {
  borderSkipped: "start",
  borderWidth: 0,
  borderRadius: 0,
  inflateAmount: "auto",
  pointStyle: void 0
}), Z(Ri, "defaultRoutes", {
  backgroundColor: "backgroundColor",
  borderColor: "borderColor"
});
function z_(e, t, n) {
  const s = e.segments, i = e.points, o = t.points, r = [];
  for (const a of s) {
    let { start: l, end: c } = a;
    c = wa(l, c, i);
    const f = Vr(n, i[l], i[c], a.loop);
    if (!t.segments) {
      r.push({
        source: a,
        target: f,
        start: i[l],
        end: i[c]
      });
      continue;
    }
    const u = Wu(t, f);
    for (const h of u) {
      const d = Vr(n, o[h.start], o[h.end], h.loop), p = Hu(a, i, d);
      for (const g of p)
        r.push({
          source: g,
          target: h,
          start: {
            [n]: wc(f, d, "start", Math.max)
          },
          end: {
            [n]: wc(f, d, "end", Math.min)
          }
        });
    }
  }
  return r;
}
function Vr(e, t, n, s) {
  if (s)
    return;
  let i = t[e], o = n[e];
  return e === "angle" && (i = Oe(i), o = Oe(o)), {
    property: e,
    start: i,
    end: o
  };
}
function H_(e, t) {
  const { x: n = null, y: s = null } = e || {}, i = t.points, o = [];
  return t.segments.forEach(({ start: r, end: a }) => {
    a = wa(r, a, i);
    const l = i[r], c = i[a];
    s !== null ? (o.push({
      x: l.x,
      y: s
    }), o.push({
      x: c.x,
      y: s
    })) : n !== null && (o.push({
      x: n,
      y: l.y
    }), o.push({
      x: n,
      y: c.y
    }));
  }), o;
}
function wa(e, t, n) {
  for (; t > e; t--) {
    const s = n[t];
    if (!isNaN(s.x) && !isNaN(s.y))
      break;
  }
  return t;
}
function wc(e, t, n, s) {
  return e && t ? s(e[n], t[n]) : e ? e[n] : t ? t[n] : 0;
}
function rh(e, t) {
  let n = [], s = !1;
  return Mt(e) ? (s = !0, n = e) : n = H_(e, t), n.length ? new wn({
    points: n,
    options: {
      tension: 0
    },
    _loop: s,
    _fullLoop: s
  }) : null;
}
function Ec(e) {
  return e && e.fill !== !1;
}
function W_(e, t, n) {
  let i = e[t].fill;
  const o = [
    t
  ];
  let r;
  if (!n)
    return i;
  for (; i !== !1 && o.indexOf(i) === -1; ) {
    if (!Rt(i))
      return i;
    if (r = e[i], !r)
      return !1;
    if (r.visible)
      return i;
    o.push(i), i = r.fill;
  }
  return !1;
}
function U_(e, t, n) {
  const s = X_(e);
  if (ot(s))
    return isNaN(s.value) ? !1 : s;
  let i = parseFloat(s);
  return Rt(i) && Math.floor(i) === i ? Y_(s[0], t, i, n) : [
    "origin",
    "start",
    "end",
    "stack",
    "shape"
  ].indexOf(s) >= 0 && s;
}
function Y_(e, t, n, s) {
  return (e === "-" || e === "+") && (n = t + n), n === t || n < 0 || n >= s ? !1 : n;
}
function K_(e, t) {
  let n = null;
  return e === "start" ? n = t.bottom : e === "end" ? n = t.top : ot(e) ? n = t.getPixelForValue(e.value) : t.getBasePixel && (n = t.getBasePixel()), n;
}
function q_(e, t, n) {
  let s;
  return e === "start" ? s = n : e === "end" ? s = t.options.reverse ? t.min : t.max : ot(e) ? s = e.value : s = t.getBaseValue(), s;
}
function X_(e) {
  const t = e.options, n = t.fill;
  let s = ht(n && n.target, n);
  return s === void 0 && (s = !!t.backgroundColor), s === !1 || s === null ? !1 : s === !0 ? "origin" : s;
}
function G_(e) {
  const { scale: t, index: n, line: s } = e, i = [], o = s.segments, r = s.points, a = Z_(t, n);
  a.push(rh({
    x: null,
    y: t.bottom
  }, s));
  for (let l = 0; l < o.length; l++) {
    const c = o[l];
    for (let f = c.start; f <= c.end; f++)
      J_(i, r[f], a);
  }
  return new wn({
    points: i,
    options: {}
  });
}
function Z_(e, t) {
  const n = [], s = e.getMatchingVisibleMetas("line");
  for (let i = 0; i < s.length; i++) {
    const o = s[i];
    if (o.index === t)
      break;
    o.hidden || n.unshift(o.dataset);
  }
  return n;
}
function J_(e, t, n) {
  const s = [];
  for (let i = 0; i < n.length; i++) {
    const o = n[i], { first: r, last: a, point: l } = Q_(o, t, "x");
    if (!(!l || r && a)) {
      if (r)
        s.unshift(l);
      else if (e.push(l), !a)
        break;
    }
  }
  e.push(...s);
}
function Q_(e, t, n) {
  const s = e.interpolate(t, n);
  if (!s)
    return {};
  const i = s[n], o = e.segments, r = e.points;
  let a = !1, l = !1;
  for (let c = 0; c < o.length; c++) {
    const f = o[c], u = r[f.start][n], h = r[f.end][n];
    if (Ji(i, u, h)) {
      a = i === u, l = i === h;
      break;
    }
  }
  return {
    first: a,
    last: l,
    point: s
  };
}
class ah {
  constructor(t) {
    this.x = t.x, this.y = t.y, this.radius = t.radius;
  }
  pathSegment(t, n, s) {
    const { x: i, y: o, radius: r } = this;
    return n = n || {
      start: 0,
      end: Ce
    }, t.arc(i, o, r, n.end, n.start, !0), !s.bounds;
  }
  interpolate(t) {
    const { x: n, y: s, radius: i } = this, o = t.angle;
    return {
      x: n + Math.cos(o) * i,
      y: s + Math.sin(o) * i,
      angle: o
    };
  }
}
function ty(e) {
  const { chart: t, fill: n, line: s } = e;
  if (Rt(n))
    return ey(t, n);
  if (n === "stack")
    return G_(e);
  if (n === "shape")
    return !0;
  const i = ny(e);
  return i instanceof ah ? i : rh(i, s);
}
function ey(e, t) {
  const n = e.getDatasetMeta(t);
  return n && e.isDatasetVisible(t) ? n.dataset : null;
}
function ny(e) {
  return (e.scale || {}).getPointPositionForValue ? iy(e) : sy(e);
}
function sy(e) {
  const { scale: t = {}, fill: n } = e, s = K_(n, t);
  if (Rt(s)) {
    const i = t.isHorizontal();
    return {
      x: i ? s : null,
      y: i ? null : s
    };
  }
  return null;
}
function iy(e) {
  const { scale: t, fill: n } = e, s = t.options, i = t.getLabels().length, o = s.reverse ? t.max : t.min, r = q_(n, t, o), a = [];
  if (s.grid.circular) {
    const l = t.getPointPositionForValue(0, o);
    return new ah({
      x: l.x,
      y: l.y,
      radius: t.getDistanceFromCenterForValue(r)
    });
  }
  for (let l = 0; l < i; ++l)
    a.push(t.getPointPositionForValue(l, r));
  return a;
}
function Go(e, t, n) {
  const s = ty(t), { line: i, scale: o, axis: r } = t, a = i.options, l = a.fill, c = a.backgroundColor, { above: f = c, below: u = c } = l || {};
  s && i.points.length && (pa(e, n), oy(e, {
    line: i,
    target: s,
    above: f,
    below: u,
    area: n,
    scale: o,
    axis: r
  }), ga(e));
}
function oy(e, t) {
  const { line: n, target: s, above: i, below: o, area: r, scale: a } = t, l = n._loop ? "angle" : t.axis;
  e.save(), l === "x" && o !== i && (Oc(e, s, r.top), Sc(e, {
    line: n,
    target: s,
    color: i,
    scale: a,
    property: l
  }), e.restore(), e.save(), Oc(e, s, r.bottom)), Sc(e, {
    line: n,
    target: s,
    color: o,
    scale: a,
    property: l
  }), e.restore();
}
function Oc(e, t, n) {
  const { segments: s, points: i } = t;
  let o = !0, r = !1;
  e.beginPath();
  for (const a of s) {
    const { start: l, end: c } = a, f = i[l], u = i[wa(l, c, i)];
    o ? (e.moveTo(f.x, f.y), o = !1) : (e.lineTo(f.x, n), e.lineTo(f.x, f.y)), r = !!t.pathSegment(e, a, {
      move: r
    }), r ? e.closePath() : e.lineTo(u.x, n);
  }
  e.lineTo(t.first().x, n), e.closePath(), e.clip();
}
function Sc(e, t) {
  const { line: n, target: s, property: i, color: o, scale: r } = t, a = z_(n, s, i);
  for (const { source: l, target: c, start: f, end: u } of a) {
    const { style: { backgroundColor: h = o } = {} } = l, d = s !== !0;
    e.save(), e.fillStyle = h, ry(e, r, d && Vr(i, f, u)), e.beginPath();
    const p = !!n.pathSegment(e, l);
    let g;
    if (d) {
      p ? e.closePath() : Mc(e, s, u, i);
      const b = !!s.pathSegment(e, c, {
        move: p,
        reverse: !0
      });
      g = p && b, g || Mc(e, s, f, i);
    }
    e.closePath(), e.fill(g ? "evenodd" : "nonzero"), e.restore();
  }
}
function ry(e, t, n) {
  const { top: s, bottom: i } = t.chart.chartArea, { property: o, start: r, end: a } = n || {};
  o === "x" && (e.beginPath(), e.rect(r, s, a - r, i - s), e.clip());
}
function Mc(e, t, n, s) {
  const i = t.interpolate(n, s);
  i && e.lineTo(i.x, i.y);
}
var ay = {
  id: "filler",
  afterDatasetsUpdate(e, t, n) {
    const s = (e.data.datasets || []).length, i = [];
    let o, r, a, l;
    for (r = 0; r < s; ++r)
      o = e.getDatasetMeta(r), a = o.dataset, l = null, a && a.options && a instanceof wn && (l = {
        visible: e.isDatasetVisible(r),
        index: r,
        fill: U_(a, r, s),
        chart: e,
        axis: o.controller.options.indexAxis,
        scale: o.vScale,
        line: a
      }), o.$filler = l, i.push(l);
    for (r = 0; r < s; ++r)
      l = i[r], !(!l || l.fill === !1) && (l.fill = W_(i, r, n.propagate));
  },
  beforeDraw(e, t, n) {
    const s = n.drawTime === "beforeDraw", i = e.getSortedVisibleDatasetMetas(), o = e.chartArea;
    for (let r = i.length - 1; r >= 0; --r) {
      const a = i[r].$filler;
      a && (a.line.updateControlPoints(o, a.axis), s && a.fill && Go(e.ctx, a, o));
    }
  },
  beforeDatasetsDraw(e, t, n) {
    if (n.drawTime !== "beforeDatasetsDraw")
      return;
    const s = e.getSortedVisibleDatasetMetas();
    for (let i = s.length - 1; i >= 0; --i) {
      const o = s[i].$filler;
      Ec(o) && Go(e.ctx, o, e.chartArea);
    }
  },
  beforeDatasetDraw(e, t, n) {
    const s = t.meta.$filler;
    !Ec(s) || n.drawTime !== "beforeDatasetDraw" || Go(e.ctx, s, e.chartArea);
  },
  defaults: {
    propagate: !0,
    drawTime: "beforeDatasetDraw"
  }
};
const ws = {
  average(e) {
    if (!e.length)
      return !1;
    let t, n, s = /* @__PURE__ */ new Set(), i = 0, o = 0;
    for (t = 0, n = e.length; t < n; ++t) {
      const a = e[t].element;
      if (a && a.hasValue()) {
        const l = a.tooltipPosition();
        s.add(l.x), i += l.y, ++o;
      }
    }
    return o === 0 || s.size === 0 ? !1 : {
      x: [
        ...s
      ].reduce((a, l) => a + l) / s.size,
      y: i / o
    };
  },
  nearest(e, t) {
    if (!e.length)
      return !1;
    let n = t.x, s = t.y, i = Number.POSITIVE_INFINITY, o, r, a;
    for (o = 0, r = e.length; o < r; ++o) {
      const l = e[o].element;
      if (l && l.hasValue()) {
        const c = l.getCenterPoint(), f = Mr(t, c);
        f < i && (i = f, a = l);
      }
    }
    if (a) {
      const l = a.tooltipPosition();
      n = l.x, s = l.y;
    }
    return {
      x: n,
      y: s
    };
  }
};
function ve(e, t) {
  return t && (Mt(t) ? Array.prototype.push.apply(e, t) : e.push(t)), e;
}
function Be(e) {
  return (typeof e == "string" || e instanceof String) && e.indexOf(`
`) > -1 ? e.split(`
`) : e;
}
function ly(e, t) {
  const { element: n, datasetIndex: s, index: i } = t, o = e.getDatasetMeta(s).controller, { label: r, value: a } = o.getLabelAndValue(i);
  return {
    chart: e,
    label: r,
    parsed: o.getParsed(i),
    raw: e.data.datasets[s].data[i],
    formattedValue: a,
    dataset: o.getDataset(),
    dataIndex: i,
    datasetIndex: s,
    element: n
  };
}
function kc(e, t) {
  const n = e.chart.ctx, { body: s, footer: i, title: o } = e, { boxWidth: r, boxHeight: a } = t, l = Ne(t.bodyFont), c = Ne(t.titleFont), f = Ne(t.footerFont), u = o.length, h = i.length, d = s.length, p = an(t.padding);
  let g = p.height, b = 0, y = s.reduce((P, w) => P + w.before.length + w.lines.length + w.after.length, 0);
  if (y += e.beforeBody.length + e.afterBody.length, u && (g += u * c.lineHeight + (u - 1) * t.titleSpacing + t.titleMarginBottom), y) {
    const P = t.displayColors ? Math.max(a, l.lineHeight) : l.lineHeight;
    g += d * P + (y - d) * l.lineHeight + (y - 1) * t.bodySpacing;
  }
  h && (g += t.footerMarginTop + h * f.lineHeight + (h - 1) * t.footerSpacing);
  let O = 0;
  const M = function(P) {
    b = Math.max(b, n.measureText(P).width + O);
  };
  return n.save(), n.font = c.string, ft(e.title, M), n.font = l.string, ft(e.beforeBody.concat(e.afterBody), M), O = t.displayColors ? r + 2 + t.boxPadding : 0, ft(s, (P) => {
    ft(P.before, M), ft(P.lines, M), ft(P.after, M);
  }), O = 0, n.font = f.string, ft(e.footer, M), n.restore(), b += p.width, {
    width: b,
    height: g
  };
}
function cy(e, t) {
  const { y: n, height: s } = t;
  return n < s / 2 ? "top" : n > e.height - s / 2 ? "bottom" : "center";
}
function fy(e, t, n, s) {
  const { x: i, width: o } = s, r = n.caretSize + n.caretPadding;
  if (e === "left" && i + o + r > t.width || e === "right" && i - o - r < 0)
    return !0;
}
function uy(e, t, n, s) {
  const { x: i, width: o } = n, { width: r, chartArea: { left: a, right: l } } = e;
  let c = "center";
  return s === "center" ? c = i <= (a + l) / 2 ? "left" : "right" : i <= o / 2 ? c = "left" : i >= r - o / 2 && (c = "right"), fy(c, e, t, n) && (c = "center"), c;
}
function Nc(e, t, n) {
  const s = n.yAlign || t.yAlign || cy(e, n);
  return {
    xAlign: n.xAlign || t.xAlign || uy(e, t, n, s),
    yAlign: s
  };
}
function hy(e, t) {
  let { x: n, width: s } = e;
  return t === "right" ? n -= s : t === "center" && (n -= s / 2), n;
}
function dy(e, t, n) {
  let { y: s, height: i } = e;
  return t === "top" ? s += n : t === "bottom" ? s -= i + n : s -= i / 2, s;
}
function Dc(e, t, n, s) {
  const { caretSize: i, caretPadding: o, cornerRadius: r } = e, { xAlign: a, yAlign: l } = n, c = i + o, { topLeft: f, topRight: u, bottomLeft: h, bottomRight: d } = As(r);
  let p = hy(t, a);
  const g = dy(t, l, c);
  return l === "center" ? a === "left" ? p += c : a === "right" && (p -= c) : a === "left" ? p -= Math.max(f, h) + i : a === "right" && (p += Math.max(u, d) + i), {
    x: he(p, 0, s.width - t.width),
    y: he(g, 0, s.height - t.height)
  };
}
function mi(e, t, n) {
  const s = an(n.padding);
  return t === "center" ? e.x + e.width / 2 : t === "right" ? e.x + e.width - s.right : e.x + s.left;
}
function Cc(e) {
  return ve([], Be(e));
}
function py(e, t, n) {
  return Vn(e, {
    tooltip: t,
    tooltipItems: n,
    type: "tooltip"
  });
}
function Pc(e, t) {
  const n = t && t.dataset && t.dataset.tooltip && t.dataset.tooltip.callbacks;
  return n ? e.override(n) : e;
}
const lh = {
  beforeTitle: Le,
  title(e) {
    if (e.length > 0) {
      const t = e[0], n = t.chart.data.labels, s = n ? n.length : 0;
      if (this && this.options && this.options.mode === "dataset")
        return t.dataset.label || "";
      if (t.label)
        return t.label;
      if (s > 0 && t.dataIndex < s)
        return n[t.dataIndex];
    }
    return "";
  },
  afterTitle: Le,
  beforeBody: Le,
  beforeLabel: Le,
  label(e) {
    if (this && this.options && this.options.mode === "dataset")
      return e.label + ": " + e.formattedValue || e.formattedValue;
    let t = e.dataset.label || "";
    t && (t += ": ");
    const n = e.formattedValue;
    return gt(n) || (t += n), t;
  },
  labelColor(e) {
    const n = e.chart.getDatasetMeta(e.datasetIndex).controller.getStyle(e.dataIndex);
    return {
      borderColor: n.borderColor,
      backgroundColor: n.backgroundColor,
      borderWidth: n.borderWidth,
      borderDash: n.borderDash,
      borderDashOffset: n.borderDashOffset,
      borderRadius: 0
    };
  },
  labelTextColor() {
    return this.options.bodyColor;
  },
  labelPointStyle(e) {
    const n = e.chart.getDatasetMeta(e.datasetIndex).controller.getStyle(e.dataIndex);
    return {
      pointStyle: n.pointStyle,
      rotation: n.rotation
    };
  },
  afterLabel: Le,
  afterBody: Le,
  beforeFooter: Le,
  footer: Le,
  afterFooter: Le
};
function Ht(e, t, n, s) {
  const i = e[t].call(n, s);
  return typeof i > "u" ? lh[t].call(n, s) : i;
}
class Rr extends Qn {
  constructor(t) {
    super(), this.opacity = 0, this._active = [], this._eventPosition = void 0, this._size = void 0, this._cachedAnimations = void 0, this._tooltipItems = [], this.$animations = void 0, this.$context = void 0, this.chart = t.chart, this.options = t.options, this.dataPoints = void 0, this.title = void 0, this.beforeBody = void 0, this.body = void 0, this.afterBody = void 0, this.footer = void 0, this.xAlign = void 0, this.yAlign = void 0, this.x = void 0, this.y = void 0, this.height = void 0, this.width = void 0, this.caretX = void 0, this.caretY = void 0, this.labelColors = void 0, this.labelPointStyles = void 0, this.labelTextColors = void 0;
  }
  initialize(t) {
    this.options = t, this._cachedAnimations = void 0, this.$context = void 0;
  }
  _resolveAnimations() {
    const t = this._cachedAnimations;
    if (t)
      return t;
    const n = this.chart, s = this.options.setContext(this.getContext()), i = s.enabled && n.options.animation && s.animations, o = new Uu(this.chart, i);
    return i._cacheable && (this._cachedAnimations = Object.freeze(o)), o;
  }
  getContext() {
    return this.$context || (this.$context = py(this.chart.getContext(), this, this._tooltipItems));
  }
  getTitle(t, n) {
    const { callbacks: s } = n, i = Ht(s, "beforeTitle", this, t), o = Ht(s, "title", this, t), r = Ht(s, "afterTitle", this, t);
    let a = [];
    return a = ve(a, Be(i)), a = ve(a, Be(o)), a = ve(a, Be(r)), a;
  }
  getBeforeBody(t, n) {
    return Cc(Ht(n.callbacks, "beforeBody", this, t));
  }
  getBody(t, n) {
    const { callbacks: s } = n, i = [];
    return ft(t, (o) => {
      const r = {
        before: [],
        lines: [],
        after: []
      }, a = Pc(s, o);
      ve(r.before, Be(Ht(a, "beforeLabel", this, o))), ve(r.lines, Ht(a, "label", this, o)), ve(r.after, Be(Ht(a, "afterLabel", this, o))), i.push(r);
    }), i;
  }
  getAfterBody(t, n) {
    return Cc(Ht(n.callbacks, "afterBody", this, t));
  }
  getFooter(t, n) {
    const { callbacks: s } = n, i = Ht(s, "beforeFooter", this, t), o = Ht(s, "footer", this, t), r = Ht(s, "afterFooter", this, t);
    let a = [];
    return a = ve(a, Be(i)), a = ve(a, Be(o)), a = ve(a, Be(r)), a;
  }
  _createItems(t) {
    const n = this._active, s = this.chart.data, i = [], o = [], r = [];
    let a = [], l, c;
    for (l = 0, c = n.length; l < c; ++l)
      a.push(ly(this.chart, n[l]));
    return t.filter && (a = a.filter((f, u, h) => t.filter(f, u, h, s))), t.itemSort && (a = a.sort((f, u) => t.itemSort(f, u, s))), ft(a, (f) => {
      const u = Pc(t.callbacks, f);
      i.push(Ht(u, "labelColor", this, f)), o.push(Ht(u, "labelPointStyle", this, f)), r.push(Ht(u, "labelTextColor", this, f));
    }), this.labelColors = i, this.labelPointStyles = o, this.labelTextColors = r, this.dataPoints = a, a;
  }
  update(t, n) {
    const s = this.options.setContext(this.getContext()), i = this._active;
    let o, r = [];
    if (!i.length)
      this.opacity !== 0 && (o = {
        opacity: 0
      });
    else {
      const a = ws[s.position].call(this, i, this._eventPosition);
      r = this._createItems(s), this.title = this.getTitle(r, s), this.beforeBody = this.getBeforeBody(r, s), this.body = this.getBody(r, s), this.afterBody = this.getAfterBody(r, s), this.footer = this.getFooter(r, s);
      const l = this._size = kc(this, s), c = Object.assign({}, a, l), f = Nc(this.chart, s, c), u = Dc(s, c, f, this.chart);
      this.xAlign = f.xAlign, this.yAlign = f.yAlign, o = {
        opacity: 1,
        x: u.x,
        y: u.y,
        width: l.width,
        height: l.height,
        caretX: a.x,
        caretY: a.y
      };
    }
    this._tooltipItems = r, this.$context = void 0, o && this._resolveAnimations().update(this, o), t && s.external && s.external.call(this, {
      chart: this.chart,
      tooltip: this,
      replay: n
    });
  }
  drawCaret(t, n, s, i) {
    const o = this.getCaretPosition(t, s, i);
    n.lineTo(o.x1, o.y1), n.lineTo(o.x2, o.y2), n.lineTo(o.x3, o.y3);
  }
  getCaretPosition(t, n, s) {
    const { xAlign: i, yAlign: o } = this, { caretSize: r, cornerRadius: a } = s, { topLeft: l, topRight: c, bottomLeft: f, bottomRight: u } = As(a), { x: h, y: d } = t, { width: p, height: g } = n;
    let b, y, O, M, P, w;
    return o === "center" ? (P = d + g / 2, i === "left" ? (b = h, y = b - r, M = P + r, w = P - r) : (b = h + p, y = b + r, M = P - r, w = P + r), O = b) : (i === "left" ? y = h + Math.max(l, f) + r : i === "right" ? y = h + p - Math.max(c, u) - r : y = this.caretX, o === "top" ? (M = d, P = M - r, b = y - r, O = y + r) : (M = d + g, P = M + r, b = y + r, O = y - r), w = M), {
      x1: b,
      x2: y,
      x3: O,
      y1: M,
      y2: P,
      y3: w
    };
  }
  drawTitle(t, n, s) {
    const i = this.title, o = i.length;
    let r, a, l;
    if (o) {
      const c = Bo(s.rtl, this.x, this.width);
      for (t.x = mi(this, s.titleAlign, s), n.textAlign = c.textAlign(s.titleAlign), n.textBaseline = "middle", r = Ne(s.titleFont), a = s.titleSpacing, n.fillStyle = s.titleColor, n.font = r.string, l = 0; l < o; ++l)
        n.fillText(i[l], c.x(t.x), t.y + r.lineHeight / 2), t.y += r.lineHeight + a, l + 1 === o && (t.y += s.titleMarginBottom - a);
    }
  }
  _drawColorBox(t, n, s, i, o) {
    const r = this.labelColors[s], a = this.labelPointStyles[s], { boxHeight: l, boxWidth: c } = o, f = Ne(o.bodyFont), u = mi(this, "left", o), h = i.x(u), d = l < f.lineHeight ? (f.lineHeight - l) / 2 : 0, p = n.y + d;
    if (o.usePointStyle) {
      const g = {
        radius: Math.min(c, l) / 2,
        pointStyle: a.pointStyle,
        rotation: a.rotation,
        borderWidth: 1
      }, b = i.leftForLtr(h, c) + c / 2, y = p + l / 2;
      t.strokeStyle = o.multiKeyBackground, t.fillStyle = o.multiKeyBackground, Dr(t, g, b, y), t.strokeStyle = r.borderColor, t.fillStyle = r.backgroundColor, Dr(t, g, b, y);
    } else {
      t.lineWidth = ot(r.borderWidth) ? Math.max(...Object.values(r.borderWidth)) : r.borderWidth || 1, t.strokeStyle = r.borderColor, t.setLineDash(r.borderDash || []), t.lineDashOffset = r.borderDashOffset || 0;
      const g = i.leftForLtr(h, c), b = i.leftForLtr(i.xPlus(h, 1), c - 2), y = As(r.borderRadius);
      Object.values(y).some((O) => O !== 0) ? (t.beginPath(), t.fillStyle = o.multiKeyBackground, Cr(t, {
        x: g,
        y: p,
        w: c,
        h: l,
        radius: y
      }), t.fill(), t.stroke(), t.fillStyle = r.backgroundColor, t.beginPath(), Cr(t, {
        x: b,
        y: p + 1,
        w: c - 2,
        h: l - 2,
        radius: y
      }), t.fill()) : (t.fillStyle = o.multiKeyBackground, t.fillRect(g, p, c, l), t.strokeRect(g, p, c, l), t.fillStyle = r.backgroundColor, t.fillRect(b, p + 1, c - 2, l - 2));
    }
    t.fillStyle = this.labelTextColors[s];
  }
  drawBody(t, n, s) {
    const { body: i } = this, { bodySpacing: o, bodyAlign: r, displayColors: a, boxHeight: l, boxWidth: c, boxPadding: f } = s, u = Ne(s.bodyFont);
    let h = u.lineHeight, d = 0;
    const p = Bo(s.rtl, this.x, this.width), g = function(S) {
      n.fillText(S, p.x(t.x + d), t.y + h / 2), t.y += h + o;
    }, b = p.textAlign(r);
    let y, O, M, P, w, k, v;
    for (n.textAlign = r, n.textBaseline = "middle", n.font = u.string, t.x = mi(this, b, s), n.fillStyle = s.bodyColor, ft(this.beforeBody, g), d = a && b !== "right" ? r === "center" ? c / 2 + f : c + 2 + f : 0, P = 0, k = i.length; P < k; ++P) {
      for (y = i[P], O = this.labelTextColors[P], n.fillStyle = O, ft(y.before, g), M = y.lines, a && M.length && (this._drawColorBox(n, t, P, p, s), h = Math.max(u.lineHeight, l)), w = 0, v = M.length; w < v; ++w)
        g(M[w]), h = u.lineHeight;
      ft(y.after, g);
    }
    d = 0, h = u.lineHeight, ft(this.afterBody, g), t.y -= o;
  }
  drawFooter(t, n, s) {
    const i = this.footer, o = i.length;
    let r, a;
    if (o) {
      const l = Bo(s.rtl, this.x, this.width);
      for (t.x = mi(this, s.footerAlign, s), t.y += s.footerMarginTop, n.textAlign = l.textAlign(s.footerAlign), n.textBaseline = "middle", r = Ne(s.footerFont), n.fillStyle = s.footerColor, n.font = r.string, a = 0; a < o; ++a)
        n.fillText(i[a], l.x(t.x), t.y + r.lineHeight / 2), t.y += r.lineHeight + s.footerSpacing;
    }
  }
  drawBackground(t, n, s, i) {
    const { xAlign: o, yAlign: r } = this, { x: a, y: l } = t, { width: c, height: f } = s, { topLeft: u, topRight: h, bottomLeft: d, bottomRight: p } = As(i.cornerRadius);
    n.fillStyle = i.backgroundColor, n.strokeStyle = i.borderColor, n.lineWidth = i.borderWidth, n.beginPath(), n.moveTo(a + u, l), r === "top" && this.drawCaret(t, n, s, i), n.lineTo(a + c - h, l), n.quadraticCurveTo(a + c, l, a + c, l + h), r === "center" && o === "right" && this.drawCaret(t, n, s, i), n.lineTo(a + c, l + f - p), n.quadraticCurveTo(a + c, l + f, a + c - p, l + f), r === "bottom" && this.drawCaret(t, n, s, i), n.lineTo(a + d, l + f), n.quadraticCurveTo(a, l + f, a, l + f - d), r === "center" && o === "left" && this.drawCaret(t, n, s, i), n.lineTo(a, l + u), n.quadraticCurveTo(a, l, a + u, l), n.closePath(), n.fill(), i.borderWidth > 0 && n.stroke();
  }
  _updateAnimationTarget(t) {
    const n = this.chart, s = this.$animations, i = s && s.x, o = s && s.y;
    if (i || o) {
      const r = ws[t.position].call(this, this._active, this._eventPosition);
      if (!r)
        return;
      const a = this._size = kc(this, t), l = Object.assign({}, r, this._size), c = Nc(n, t, l), f = Dc(t, l, c, n);
      (i._to !== f.x || o._to !== f.y) && (this.xAlign = c.xAlign, this.yAlign = c.yAlign, this.width = a.width, this.height = a.height, this.caretX = r.x, this.caretY = r.y, this._resolveAnimations().update(this, f));
    }
  }
  _willRender() {
    return !!this.opacity;
  }
  draw(t) {
    const n = this.options.setContext(this.getContext());
    let s = this.opacity;
    if (!s)
      return;
    this._updateAnimationTarget(n);
    const i = {
      width: this.width,
      height: this.height
    }, o = {
      x: this.x,
      y: this.y
    };
    s = Math.abs(s) < 1e-3 ? 0 : s;
    const r = an(n.padding), a = this.title.length || this.beforeBody.length || this.body.length || this.afterBody.length || this.footer.length;
    n.enabled && a && (t.save(), t.globalAlpha = s, this.drawBackground(o, t, i, n), B0(t, n.textDirection), o.y += r.top, this.drawTitle(o, t, n), this.drawBody(o, t, n), this.drawFooter(o, t, n), j0(t, n.textDirection), t.restore());
  }
  getActiveElements() {
    return this._active || [];
  }
  setActiveElements(t, n) {
    const s = this._active, i = t.map(({ datasetIndex: a, index: l }) => {
      const c = this.chart.getDatasetMeta(a);
      if (!c)
        throw new Error("Cannot find a dataset at index " + a);
      return {
        datasetIndex: a,
        element: c.data[l],
        index: l
      };
    }), o = !qi(s, i), r = this._positionChanged(i, n);
    (o || r) && (this._active = i, this._eventPosition = n, this._ignoreReplayEvents = !0, this.update(!0));
  }
  handleEvent(t, n, s = !0) {
    if (n && this._ignoreReplayEvents)
      return !1;
    this._ignoreReplayEvents = !1;
    const i = this.options, o = this._active || [], r = this._getActiveElements(t, o, n, s), a = this._positionChanged(r, t), l = n || !qi(r, o) || a;
    return l && (this._active = r, (i.enabled || i.external) && (this._eventPosition = {
      x: t.x,
      y: t.y
    }, this.update(!0, n))), l;
  }
  _getActiveElements(t, n, s, i) {
    const o = this.options;
    if (t.type === "mouseout")
      return [];
    if (!i)
      return n.filter((a) => this.chart.data.datasets[a.datasetIndex] && this.chart.getDatasetMeta(a.datasetIndex).controller.getParsed(a.index) !== void 0);
    const r = this.chart.getElementsAtEventForMode(t, o.mode, o, s);
    return o.reverse && r.reverse(), r;
  }
  _positionChanged(t, n) {
    const { caretX: s, caretY: i, options: o } = this, r = ws[o.position].call(this, t, n);
    return r !== !1 && (s !== r.x || i !== r.y);
  }
}
Z(Rr, "positioners", ws);
var gy = {
  id: "tooltip",
  _element: Rr,
  positioners: ws,
  afterInit(e, t, n) {
    n && (e.tooltip = new Rr({
      chart: e,
      options: n
    }));
  },
  beforeUpdate(e, t, n) {
    e.tooltip && e.tooltip.initialize(n);
  },
  reset(e, t, n) {
    e.tooltip && e.tooltip.initialize(n);
  },
  afterDraw(e) {
    const t = e.tooltip;
    if (t && t._willRender()) {
      const n = {
        tooltip: t
      };
      if (e.notifyPlugins("beforeTooltipDraw", {
        ...n,
        cancelable: !0
      }) === !1)
        return;
      t.draw(e.ctx), e.notifyPlugins("afterTooltipDraw", n);
    }
  },
  afterEvent(e, t) {
    if (e.tooltip) {
      const n = t.replay;
      e.tooltip.handleEvent(t.event, n, t.inChartArea) && (t.changed = !0);
    }
  },
  defaults: {
    enabled: !0,
    external: null,
    position: "average",
    backgroundColor: "rgba(0,0,0,0.8)",
    titleColor: "#fff",
    titleFont: {
      weight: "bold"
    },
    titleSpacing: 2,
    titleMarginBottom: 6,
    titleAlign: "left",
    bodyColor: "#fff",
    bodySpacing: 2,
    bodyFont: {},
    bodyAlign: "left",
    footerColor: "#fff",
    footerSpacing: 2,
    footerMarginTop: 6,
    footerFont: {
      weight: "bold"
    },
    footerAlign: "left",
    padding: 6,
    caretPadding: 2,
    caretSize: 5,
    cornerRadius: 6,
    boxHeight: (e, t) => t.bodyFont.size,
    boxWidth: (e, t) => t.bodyFont.size,
    multiKeyBackground: "#fff",
    displayColors: !0,
    boxPadding: 0,
    borderColor: "rgba(0,0,0,0)",
    borderWidth: 0,
    animation: {
      duration: 400,
      easing: "easeOutQuart"
    },
    animations: {
      numbers: {
        type: "number",
        properties: [
          "x",
          "y",
          "width",
          "height",
          "caretX",
          "caretY"
        ]
      },
      opacity: {
        easing: "linear",
        duration: 200
      }
    },
    callbacks: lh
  },
  defaultRoutes: {
    bodyFont: "font",
    footerFont: "font",
    titleFont: "font"
  },
  descriptors: {
    _scriptable: (e) => e !== "filter" && e !== "itemSort" && e !== "external",
    _indexable: !1,
    callbacks: {
      _scriptable: !1,
      _indexable: !1
    },
    animation: {
      _fallback: !1
    },
    animations: {
      _fallback: "animation"
    }
  },
  additionalOptionScopes: [
    "interaction"
  ]
};
const my = (e, t, n, s) => (typeof t == "string" ? (n = e.push(t) - 1, s.unshift({
  index: n,
  label: t
})) : isNaN(t) && (n = null), n);
function by(e, t, n, s) {
  const i = e.indexOf(t);
  if (i === -1)
    return my(e, t, n, s);
  const o = e.lastIndexOf(t);
  return i !== o ? n : i;
}
const _y = (e, t) => e === null ? null : he(Math.round(e), 0, t);
function Tc(e) {
  const t = this.getLabels();
  return e >= 0 && e < t.length ? t[e] : e;
}
class Ir extends ts {
  constructor(t) {
    super(t), this._startValue = void 0, this._valueRange = 0, this._addedLabels = [];
  }
  init(t) {
    const n = this._addedLabels;
    if (n.length) {
      const s = this.getLabels();
      for (const { index: i, label: o } of n)
        s[i] === o && s.splice(i, 1);
      this._addedLabels = [];
    }
    super.init(t);
  }
  parse(t, n) {
    if (gt(t))
      return null;
    const s = this.getLabels();
    return n = isFinite(n) && s[n] === t ? n : by(s, t, ht(n, t), this._addedLabels), _y(n, s.length - 1);
  }
  determineDataLimits() {
    const { minDefined: t, maxDefined: n } = this.getUserBounds();
    let { min: s, max: i } = this.getMinMax(!0);
    this.options.bounds === "ticks" && (t || (s = 0), n || (i = this.getLabels().length - 1)), this.min = s, this.max = i;
  }
  buildTicks() {
    const t = this.min, n = this.max, s = this.options.offset, i = [];
    let o = this.getLabels();
    o = t === 0 && n === o.length - 1 ? o : o.slice(t, n + 1), this._valueRange = Math.max(o.length - (s ? 0 : 1), 1), this._startValue = this.min - (s ? 0.5 : 0);
    for (let r = t; r <= n; r++)
      i.push({
        value: r
      });
    return i;
  }
  getLabelForValue(t) {
    return Tc.call(this, t);
  }
  configure() {
    super.configure(), this.isHorizontal() || (this._reversePixels = !this._reversePixels);
  }
  getPixelForValue(t) {
    return typeof t != "number" && (t = this.parse(t)), t === null ? NaN : this.getPixelForDecimal((t - this._startValue) / this._valueRange);
  }
  getPixelForTick(t) {
    const n = this.ticks;
    return t < 0 || t > n.length - 1 ? null : this.getPixelForValue(n[t].value);
  }
  getValueForPixel(t) {
    return Math.round(this._startValue + this.getDecimalForPixel(t) * this._valueRange);
  }
  getBasePixel() {
    return this.bottom;
  }
}
Z(Ir, "id", "category"), Z(Ir, "defaults", {
  ticks: {
    callback: Tc
  }
});
function yy(e, t) {
  const n = [], { bounds: i, step: o, min: r, max: a, precision: l, count: c, maxTicks: f, maxDigits: u, includeBounds: h } = e, d = o || 1, p = f - 1, { min: g, max: b } = t, y = !gt(r), O = !gt(a), M = !gt(c), P = (b - g) / (u + 1);
  let w = Dl((b - g) / p / d) * d, k, v, S, D;
  if (w < 1e-14 && !y && !O)
    return [
      {
        value: g
      },
      {
        value: b
      }
    ];
  D = Math.ceil(b / w) - Math.floor(g / w), D > p && (w = Dl(D * w / p / d) * d), gt(l) || (k = Math.pow(10, l), w = Math.ceil(w * k) / k), i === "ticks" ? (v = Math.floor(g / w) * w, S = Math.ceil(b / w) * w) : (v = g, S = b), y && O && o && Rm((a - r) / o, w / 1e3) ? (D = Math.round(Math.min((a - r) / w, f)), w = (a - r) / D, v = r, S = a) : M ? (v = y ? r : v, S = O ? a : S, D = c - 1, w = (S - v) / D) : (D = (S - v) / w, Cs(D, Math.round(D), w / 1e3) ? D = Math.round(D) : D = Math.ceil(D));
  const F = Math.max(Cl(w), Cl(v));
  k = Math.pow(10, gt(l) ? F : l), v = Math.round(v * k) / k, S = Math.round(S * k) / k;
  let z = 0;
  for (y && (h && v !== r ? (n.push({
    value: r
  }), v < r && z++, Cs(Math.round((v + z * w) * k) / k, r, Ac(r, P, e)) && z++) : v < r && z++); z < D; ++z) {
    const j = Math.round((v + z * w) * k) / k;
    if (O && j > a)
      break;
    n.push({
      value: j
    });
  }
  return O && h && S !== a ? n.length && Cs(n[n.length - 1].value, a, Ac(a, P, e)) ? n[n.length - 1].value = a : n.push({
    value: a
  }) : (!O || S === a) && n.push({
    value: S
  }), n;
}
function Ac(e, t, { horizontal: n, minRotation: s }) {
  const i = vn(s), o = (n ? Math.sin(i) : Math.cos(i)) || 1e-3, r = 0.75 * t * ("" + e).length;
  return Math.min(t / o, r);
}
class xy extends ts {
  constructor(t) {
    super(t), this.start = void 0, this.end = void 0, this._startValue = void 0, this._endValue = void 0, this._valueRange = 0;
  }
  parse(t, n) {
    return gt(t) || (typeof t == "number" || t instanceof Number) && !isFinite(+t) ? null : +t;
  }
  handleTickRangeOptions() {
    const { beginAtZero: t } = this.options, { minDefined: n, maxDefined: s } = this.getUserBounds();
    let { min: i, max: o } = this;
    const r = (l) => i = n ? i : l, a = (l) => o = s ? o : l;
    if (t) {
      const l = Pe(i), c = Pe(o);
      l < 0 && c < 0 ? a(0) : l > 0 && c > 0 && r(0);
    }
    if (i === o) {
      let l = o === 0 ? 1 : Math.abs(o * 0.05);
      a(o + l), t || r(i - l);
    }
    this.min = i, this.max = o;
  }
  getTickLimit() {
    const t = this.options.ticks;
    let { maxTicksLimit: n, stepSize: s } = t, i;
    return s ? (i = Math.ceil(this.max / s) - Math.floor(this.min / s) + 1, i > 1e3 && (console.warn(`scales.${this.id}.ticks.stepSize: ${s} would result generating up to ${i} ticks. Limiting to 1000.`), i = 1e3)) : (i = this.computeTickLimit(), n = n || 11), n && (i = Math.min(n, i)), i;
  }
  computeTickLimit() {
    return Number.POSITIVE_INFINITY;
  }
  buildTicks() {
    const t = this.options, n = t.ticks;
    let s = this.getTickLimit();
    s = Math.max(2, s);
    const i = {
      maxTicks: s,
      bounds: t.bounds,
      min: t.min,
      max: t.max,
      precision: n.precision,
      step: n.stepSize,
      count: n.count,
      maxDigits: this._maxDigits(),
      horizontal: this.isHorizontal(),
      minRotation: n.minRotation || 0,
      includeBounds: n.includeBounds !== !1
    }, o = this._range || this, r = yy(i, o);
    return t.bounds === "ticks" && Im(r, this, "value"), t.reverse ? (r.reverse(), this.start = this.max, this.end = this.min) : (this.start = this.min, this.end = this.max), r;
  }
  configure() {
    const t = this.ticks;
    let n = this.min, s = this.max;
    if (super.configure(), this.options.offset && t.length) {
      const i = (s - n) / Math.max(t.length - 1, 1) / 2;
      n -= i, s += i;
    }
    this._startValue = n, this._endValue = s, this._valueRange = s - n;
  }
  getLabelForValue(t) {
    return Au(t, this.chart.options.locale, this.options.ticks.format);
  }
}
class Lr extends xy {
  determineDataLimits() {
    const { min: t, max: n } = this.getMinMax(!0);
    this.min = Rt(t) ? t : 0, this.max = Rt(n) ? n : 1, this.handleTickRangeOptions();
  }
  computeTickLimit() {
    const t = this.isHorizontal(), n = t ? this.width : this.height, s = vn(this.options.ticks.minRotation), i = (t ? Math.sin(s) : Math.cos(s)) || 1e-3, o = this._resolveTickFontOptions(0);
    return Math.ceil(n / Math.min(40, o.lineHeight / i));
  }
  getPixelForValue(t) {
    return t === null ? NaN : this.getPixelForDecimal((t - this._startValue) / this._valueRange);
  }
  getValueForPixel(t) {
    return this._startValue + this.getDecimalForPixel(t) * this._valueRange;
  }
}
Z(Lr, "id", "linear"), Z(Lr, "defaults", {
  ticks: {
    callback: Vu.formatters.numeric
  }
});
const vo = {
  millisecond: {
    common: !0,
    size: 1,
    steps: 1e3
  },
  second: {
    common: !0,
    size: 1e3,
    steps: 60
  },
  minute: {
    common: !0,
    size: 6e4,
    steps: 60
  },
  hour: {
    common: !0,
    size: 36e5,
    steps: 24
  },
  day: {
    common: !0,
    size: 864e5,
    steps: 30
  },
  week: {
    common: !1,
    size: 6048e5,
    steps: 4
  },
  month: {
    common: !0,
    size: 2628e6,
    steps: 12
  },
  quarter: {
    common: !1,
    size: 7884e6,
    steps: 4
  },
  year: {
    common: !0,
    size: 3154e7
  }
}, Yt = /* @__PURE__ */ Object.keys(vo);
function Vc(e, t) {
  return e - t;
}
function Rc(e, t) {
  if (gt(t))
    return null;
  const n = e._adapter, { parser: s, round: i, isoWeekday: o } = e._parseOpts;
  let r = t;
  return typeof s == "function" && (r = s(r)), Rt(r) || (r = typeof s == "string" ? n.parse(r, s) : n.parse(r)), r === null ? null : (i && (r = i === "week" && (Zi(o) || o === !0) ? n.startOf(r, "isoWeek", o) : n.startOf(r, i)), +r);
}
function Ic(e, t, n, s) {
  const i = Yt.length;
  for (let o = Yt.indexOf(e); o < i - 1; ++o) {
    const r = vo[Yt[o]], a = r.steps ? r.steps : Number.MAX_SAFE_INTEGER;
    if (r.common && Math.ceil((n - t) / (a * r.size)) <= s)
      return Yt[o];
  }
  return Yt[i - 1];
}
function vy(e, t, n, s, i) {
  for (let o = Yt.length - 1; o >= Yt.indexOf(n); o--) {
    const r = Yt[o];
    if (vo[r].common && e._adapter.diff(i, s, r) >= t - 1)
      return r;
  }
  return Yt[n ? Yt.indexOf(n) : 0];
}
function wy(e) {
  for (let t = Yt.indexOf(e) + 1, n = Yt.length; t < n; ++t)
    if (vo[Yt[t]].common)
      return Yt[t];
}
function Lc(e, t, n) {
  if (!n)
    e[t] = !0;
  else if (n.length) {
    const { lo: s, hi: i } = ha(n, t), o = n[s] >= t ? n[s] : n[i];
    e[o] = !0;
  }
}
function Ey(e, t, n, s) {
  const i = e._adapter, o = +i.startOf(t[0].value, s), r = t[t.length - 1].value;
  let a, l;
  for (a = o; a <= r; a = +i.add(a, 1, s))
    l = n[a], l >= 0 && (t[l].major = !0);
  return t;
}
function Fc(e, t, n) {
  const s = [], i = {}, o = t.length;
  let r, a;
  for (r = 0; r < o; ++r)
    a = t[r], i[a] = r, s.push({
      value: a,
      major: !1
    });
  return o === 0 || !n ? s : Ey(e, s, i, n);
}
class eo extends ts {
  constructor(t) {
    super(t), this._cache = {
      data: [],
      labels: [],
      all: []
    }, this._unit = "day", this._majorUnit = void 0, this._offsets = {}, this._normalized = !1, this._parseOpts = void 0;
  }
  init(t, n = {}) {
    const s = t.time || (t.time = {}), i = this._adapter = new _b._date(t.adapters.date);
    i.init(n), Ds(s.displayFormats, i.formats()), this._parseOpts = {
      parser: s.parser,
      round: s.round,
      isoWeekday: s.isoWeekday
    }, super.init(t), this._normalized = n.normalized;
  }
  parse(t, n) {
    return t === void 0 ? null : Rc(this, t);
  }
  beforeLayout() {
    super.beforeLayout(), this._cache = {
      data: [],
      labels: [],
      all: []
    };
  }
  determineDataLimits() {
    const t = this.options, n = this._adapter, s = t.time.unit || "day";
    let { min: i, max: o, minDefined: r, maxDefined: a } = this.getUserBounds();
    function l(c) {
      !r && !isNaN(c.min) && (i = Math.min(i, c.min)), !a && !isNaN(c.max) && (o = Math.max(o, c.max));
    }
    (!r || !a) && (l(this._getLabelBounds()), (t.bounds !== "ticks" || t.ticks.source !== "labels") && l(this.getMinMax(!1))), i = Rt(i) && !isNaN(i) ? i : +n.startOf(Date.now(), s), o = Rt(o) && !isNaN(o) ? o : +n.endOf(Date.now(), s) + 1, this.min = Math.min(i, o - 1), this.max = Math.max(i + 1, o);
  }
  _getLabelBounds() {
    const t = this.getLabelTimestamps();
    let n = Number.POSITIVE_INFINITY, s = Number.NEGATIVE_INFINITY;
    return t.length && (n = t[0], s = t[t.length - 1]), {
      min: n,
      max: s
    };
  }
  buildTicks() {
    const t = this.options, n = t.time, s = t.ticks, i = s.source === "labels" ? this.getLabelTimestamps() : this._generate();
    t.bounds === "ticks" && i.length && (this.min = this._userMin || i[0], this.max = this._userMax || i[i.length - 1]);
    const o = this.min, r = this.max, a = zm(i, o, r);
    return this._unit = n.unit || (s.autoSkip ? Ic(n.minUnit, this.min, this.max, this._getLabelCapacity(o)) : vy(this, a.length, n.minUnit, this.min, this.max)), this._majorUnit = !s.major.enabled || this._unit === "year" ? void 0 : wy(this._unit), this.initOffsets(i), t.reverse && a.reverse(), Fc(this, a, this._majorUnit);
  }
  afterAutoSkip() {
    this.options.offsetAfterAutoskip && this.initOffsets(this.ticks.map((t) => +t.value));
  }
  initOffsets(t = []) {
    let n = 0, s = 0, i, o;
    this.options.offset && t.length && (i = this.getDecimalForValue(t[0]), t.length === 1 ? n = 1 - i : n = (this.getDecimalForValue(t[1]) - i) / 2, o = this.getDecimalForValue(t[t.length - 1]), t.length === 1 ? s = o : s = (o - this.getDecimalForValue(t[t.length - 2])) / 2);
    const r = t.length < 3 ? 0.5 : 0.25;
    n = he(n, 0, r), s = he(s, 0, r), this._offsets = {
      start: n,
      end: s,
      factor: 1 / (n + 1 + s)
    };
  }
  _generate() {
    const t = this._adapter, n = this.min, s = this.max, i = this.options, o = i.time, r = o.unit || Ic(o.minUnit, n, s, this._getLabelCapacity(n)), a = ht(i.ticks.stepSize, 1), l = r === "week" ? o.isoWeekday : !1, c = Zi(l) || l === !0, f = {};
    let u = n, h, d;
    if (c && (u = +t.startOf(u, "isoWeek", l)), u = +t.startOf(u, c ? "day" : r), t.diff(s, n, r) > 1e5 * a)
      throw new Error(n + " and " + s + " are too far apart with stepSize of " + a + " " + r);
    const p = i.ticks.source === "data" && this.getDataTimestamps();
    for (h = u, d = 0; h < s; h = +t.add(h, a, r), d++)
      Lc(f, h, p);
    return (h === s || i.bounds === "ticks" || d === 1) && Lc(f, h, p), Object.keys(f).sort(Vc).map((g) => +g);
  }
  getLabelForValue(t) {
    const n = this._adapter, s = this.options.time;
    return s.tooltipFormat ? n.format(t, s.tooltipFormat) : n.format(t, s.displayFormats.datetime);
  }
  format(t, n) {
    const i = this.options.time.displayFormats, o = this._unit, r = n || i[o];
    return this._adapter.format(t, r);
  }
  _tickFormatFunction(t, n, s, i) {
    const o = this.options, r = o.ticks.callback;
    if (r)
      return yt(r, [
        t,
        n,
        s
      ], this);
    const a = o.time.displayFormats, l = this._unit, c = this._majorUnit, f = l && a[l], u = c && a[c], h = s[n], d = c && u && h && h.major;
    return this._adapter.format(t, i || (d ? u : f));
  }
  generateTickLabels(t) {
    let n, s, i;
    for (n = 0, s = t.length; n < s; ++n)
      i = t[n], i.label = this._tickFormatFunction(i.value, n, t);
  }
  getDecimalForValue(t) {
    return t === null ? NaN : (t - this.min) / (this.max - this.min);
  }
  getPixelForValue(t) {
    const n = this._offsets, s = this.getDecimalForValue(t);
    return this.getPixelForDecimal((n.start + s) * n.factor);
  }
  getValueForPixel(t) {
    const n = this._offsets, s = this.getDecimalForPixel(t) / n.factor - n.end;
    return this.min + s * (this.max - this.min);
  }
  _getLabelSize(t) {
    const n = this.options.ticks, s = this.ctx.measureText(t).width, i = vn(this.isHorizontal() ? n.maxRotation : n.minRotation), o = Math.cos(i), r = Math.sin(i), a = this._resolveTickFontOptions(0).size;
    return {
      w: s * o + a * r,
      h: s * r + a * o
    };
  }
  _getLabelCapacity(t) {
    const n = this.options.time, s = n.displayFormats, i = s[n.unit] || s.millisecond, o = this._tickFormatFunction(t, 0, Fc(this, [
      t
    ], this._majorUnit), i), r = this._getLabelSize(o), a = Math.floor(this.isHorizontal() ? this.width / r.w : this.height / r.h) - 1;
    return a > 0 ? a : 1;
  }
  getDataTimestamps() {
    let t = this._cache.data || [], n, s;
    if (t.length)
      return t;
    const i = this.getMatchingVisibleMetas();
    if (this._normalized && i.length)
      return this._cache.data = i[0].controller.getAllParsedValues(this);
    for (n = 0, s = i.length; n < s; ++n)
      t = t.concat(i[n].controller.getAllParsedValues(this));
    return this._cache.data = this.normalize(t);
  }
  getLabelTimestamps() {
    const t = this._cache.labels || [];
    let n, s;
    if (t.length)
      return t;
    const i = this.getLabels();
    for (n = 0, s = i.length; n < s; ++n)
      t.push(Rc(this, i[n]));
    return this._cache.labels = this._normalized ? t : this.normalize(t);
  }
  normalize(t) {
    return Cu(t.sort(Vc));
  }
}
Z(eo, "id", "time"), Z(eo, "defaults", {
  bounds: "data",
  adapters: {},
  time: {
    parser: !1,
    unit: !1,
    round: !1,
    isoWeekday: !1,
    minUnit: "millisecond",
    displayFormats: {}
  },
  ticks: {
    source: "auto",
    callback: !1,
    major: {
      enabled: !1
    }
  }
});
function bi(e, t, n) {
  let s = 0, i = e.length - 1, o, r, a, l;
  n ? (t >= e[s].pos && t <= e[i].pos && ({ lo: s, hi: i } = kr(e, "pos", t)), { pos: o, time: a } = e[s], { pos: r, time: l } = e[i]) : (t >= e[s].time && t <= e[i].time && ({ lo: s, hi: i } = kr(e, "time", t)), { time: o, pos: a } = e[s], { time: r, pos: l } = e[i]);
  const c = r - o;
  return c ? a + (l - a) * (t - o) / c : a;
}
class $c extends eo {
  constructor(t) {
    super(t), this._table = [], this._minPos = void 0, this._tableRange = void 0;
  }
  initOffsets() {
    const t = this._getTimestampsForTable(), n = this._table = this.buildLookupTable(t);
    this._minPos = bi(n, this.min), this._tableRange = bi(n, this.max) - this._minPos, super.initOffsets(t);
  }
  buildLookupTable(t) {
    const { min: n, max: s } = this, i = [], o = [];
    let r, a, l, c, f;
    for (r = 0, a = t.length; r < a; ++r)
      c = t[r], c >= n && c <= s && i.push(c);
    if (i.length < 2)
      return [
        {
          time: n,
          pos: 0
        },
        {
          time: s,
          pos: 1
        }
      ];
    for (r = 0, a = i.length; r < a; ++r)
      f = i[r + 1], l = i[r - 1], c = i[r], Math.round((f + l) / 2) !== c && o.push({
        time: c,
        pos: r / (a - 1)
      });
    return o;
  }
  _generate() {
    const t = this.min, n = this.max;
    let s = super.getDataTimestamps();
    return (!s.includes(t) || !s.length) && s.splice(0, 0, t), (!s.includes(n) || s.length === 1) && s.push(n), s.sort((i, o) => i - o);
  }
  _getTimestampsForTable() {
    let t = this._cache.all || [];
    if (t.length)
      return t;
    const n = this.getDataTimestamps(), s = this.getLabelTimestamps();
    return n.length && s.length ? t = this.normalize(n.concat(s)) : t = n.length ? n : s, t = this._cache.all = t, t;
  }
  getDecimalForValue(t) {
    return (bi(this._table, t) - this._minPos) / this._tableRange;
  }
  getValueForPixel(t) {
    const n = this._offsets, s = this.getDecimalForPixel(t) / n.factor - n.end;
    return bi(this._table, s * this._tableRange + this._minPos, !0);
  }
}
Z($c, "id", "timeseries"), Z($c, "defaults", eo.defaults);
Pt.register(gy, ay, Lr, Ir, Vi);
const Oy = (e) => e.charAt(0).toUpperCase() + e.slice(1), Sy = (e) => isNaN(e) ? e : Number.isInteger(e) ? parseInt(e).toLocaleString("fr-FR") : parseFloat(e).toLocaleString("fr-FR", { maximumFractionDigits: 2 }), My = () => {
  Pt.defaults.font.family = "Marianne", Pt.defaults.font.size = 12, Pt.defaults.font.lineHeight = 1.66, Pt.defaults.color = "#6b6b6b", Pt.defaults.borderColor = "#cecece";
}, ky = {
  methods: {
    capitalize: Oy,
    formatNumber: Sy
  }
}, { min: Ny, max: Dy } = Math, Pn = (e, t = 0, n = 1) => Ny(Dy(t, e), n), Ea = (e) => {
  e._clipped = !1, e._unclipped = e.slice(0);
  for (let t = 0; t <= 3; t++)
    t < 3 ? ((e[t] < 0 || e[t] > 255) && (e._clipped = !0), e[t] = Pn(e[t], 0, 255)) : t === 3 && (e[t] = Pn(e[t], 0, 1));
  return e;
}, ch = {};
for (let e of [
  "Boolean",
  "Number",
  "String",
  "Function",
  "Array",
  "Date",
  "RegExp",
  "Undefined",
  "Null"
])
  ch[`[object ${e}]`] = e.toLowerCase();
function nt(e) {
  return ch[Object.prototype.toString.call(e)] || "object";
}
const Q = (e, t = null) => e.length >= 3 ? Array.prototype.slice.call(e) : nt(e[0]) == "object" && t ? t.split("").filter((n) => e[0][n] !== void 0).map((n) => e[0][n]) : e[0].slice(0), es = (e) => {
  if (e.length < 2) return null;
  const t = e.length - 1;
  return nt(e[t]) == "string" ? e[t].toLowerCase() : null;
}, { PI: wo, min: fh, max: uh } = Math, ie = (e) => Math.round(e * 100) / 100, Fr = (e) => Math.round(e * 100) / 100, He = wo * 2, Zo = wo / 3, Cy = wo / 180, Py = 180 / wo;
function hh(e) {
  return [...e.slice(0, 3).reverse(), ...e.slice(3)];
}
const J = {
  format: {},
  autodetect: []
};
class V {
  constructor(...t) {
    const n = this;
    if (nt(t[0]) === "object" && t[0].constructor && t[0].constructor === this.constructor)
      return t[0];
    let s = es(t), i = !1;
    if (!s) {
      i = !0, J.sorted || (J.autodetect = J.autodetect.sort((o, r) => r.p - o.p), J.sorted = !0);
      for (let o of J.autodetect)
        if (s = o.test(...t), s) break;
    }
    if (J.format[s]) {
      const o = J.format[s].apply(
        null,
        i ? t : t.slice(0, -1)
      );
      n._rgb = Ea(o);
    } else
      throw new Error("unknown format: " + t);
    n._rgb.length === 3 && n._rgb.push(1);
  }
  toString() {
    return nt(this.hex) == "function" ? this.hex() : `[${this._rgb.join(",")}]`;
  }
}
const Ty = "3.1.2", q = (...e) => new V(...e);
q.version = Ty;
const Gn = {
  aliceblue: "#f0f8ff",
  antiquewhite: "#faebd7",
  aqua: "#00ffff",
  aquamarine: "#7fffd4",
  azure: "#f0ffff",
  beige: "#f5f5dc",
  bisque: "#ffe4c4",
  black: "#000000",
  blanchedalmond: "#ffebcd",
  blue: "#0000ff",
  blueviolet: "#8a2be2",
  brown: "#a52a2a",
  burlywood: "#deb887",
  cadetblue: "#5f9ea0",
  chartreuse: "#7fff00",
  chocolate: "#d2691e",
  coral: "#ff7f50",
  cornflowerblue: "#6495ed",
  cornsilk: "#fff8dc",
  crimson: "#dc143c",
  cyan: "#00ffff",
  darkblue: "#00008b",
  darkcyan: "#008b8b",
  darkgoldenrod: "#b8860b",
  darkgray: "#a9a9a9",
  darkgreen: "#006400",
  darkgrey: "#a9a9a9",
  darkkhaki: "#bdb76b",
  darkmagenta: "#8b008b",
  darkolivegreen: "#556b2f",
  darkorange: "#ff8c00",
  darkorchid: "#9932cc",
  darkred: "#8b0000",
  darksalmon: "#e9967a",
  darkseagreen: "#8fbc8f",
  darkslateblue: "#483d8b",
  darkslategray: "#2f4f4f",
  darkslategrey: "#2f4f4f",
  darkturquoise: "#00ced1",
  darkviolet: "#9400d3",
  deeppink: "#ff1493",
  deepskyblue: "#00bfff",
  dimgray: "#696969",
  dimgrey: "#696969",
  dodgerblue: "#1e90ff",
  firebrick: "#b22222",
  floralwhite: "#fffaf0",
  forestgreen: "#228b22",
  fuchsia: "#ff00ff",
  gainsboro: "#dcdcdc",
  ghostwhite: "#f8f8ff",
  gold: "#ffd700",
  goldenrod: "#daa520",
  gray: "#808080",
  green: "#008000",
  greenyellow: "#adff2f",
  grey: "#808080",
  honeydew: "#f0fff0",
  hotpink: "#ff69b4",
  indianred: "#cd5c5c",
  indigo: "#4b0082",
  ivory: "#fffff0",
  khaki: "#f0e68c",
  laserlemon: "#ffff54",
  lavender: "#e6e6fa",
  lavenderblush: "#fff0f5",
  lawngreen: "#7cfc00",
  lemonchiffon: "#fffacd",
  lightblue: "#add8e6",
  lightcoral: "#f08080",
  lightcyan: "#e0ffff",
  lightgoldenrod: "#fafad2",
  lightgoldenrodyellow: "#fafad2",
  lightgray: "#d3d3d3",
  lightgreen: "#90ee90",
  lightgrey: "#d3d3d3",
  lightpink: "#ffb6c1",
  lightsalmon: "#ffa07a",
  lightseagreen: "#20b2aa",
  lightskyblue: "#87cefa",
  lightslategray: "#778899",
  lightslategrey: "#778899",
  lightsteelblue: "#b0c4de",
  lightyellow: "#ffffe0",
  lime: "#00ff00",
  limegreen: "#32cd32",
  linen: "#faf0e6",
  magenta: "#ff00ff",
  maroon: "#800000",
  maroon2: "#7f0000",
  maroon3: "#b03060",
  mediumaquamarine: "#66cdaa",
  mediumblue: "#0000cd",
  mediumorchid: "#ba55d3",
  mediumpurple: "#9370db",
  mediumseagreen: "#3cb371",
  mediumslateblue: "#7b68ee",
  mediumspringgreen: "#00fa9a",
  mediumturquoise: "#48d1cc",
  mediumvioletred: "#c71585",
  midnightblue: "#191970",
  mintcream: "#f5fffa",
  mistyrose: "#ffe4e1",
  moccasin: "#ffe4b5",
  navajowhite: "#ffdead",
  navy: "#000080",
  oldlace: "#fdf5e6",
  olive: "#808000",
  olivedrab: "#6b8e23",
  orange: "#ffa500",
  orangered: "#ff4500",
  orchid: "#da70d6",
  palegoldenrod: "#eee8aa",
  palegreen: "#98fb98",
  paleturquoise: "#afeeee",
  palevioletred: "#db7093",
  papayawhip: "#ffefd5",
  peachpuff: "#ffdab9",
  peru: "#cd853f",
  pink: "#ffc0cb",
  plum: "#dda0dd",
  powderblue: "#b0e0e6",
  purple: "#800080",
  purple2: "#7f007f",
  purple3: "#a020f0",
  rebeccapurple: "#663399",
  red: "#ff0000",
  rosybrown: "#bc8f8f",
  royalblue: "#4169e1",
  saddlebrown: "#8b4513",
  salmon: "#fa8072",
  sandybrown: "#f4a460",
  seagreen: "#2e8b57",
  seashell: "#fff5ee",
  sienna: "#a0522d",
  silver: "#c0c0c0",
  skyblue: "#87ceeb",
  slateblue: "#6a5acd",
  slategray: "#708090",
  slategrey: "#708090",
  snow: "#fffafa",
  springgreen: "#00ff7f",
  steelblue: "#4682b4",
  tan: "#d2b48c",
  teal: "#008080",
  thistle: "#d8bfd8",
  tomato: "#ff6347",
  turquoise: "#40e0d0",
  violet: "#ee82ee",
  wheat: "#f5deb3",
  white: "#ffffff",
  whitesmoke: "#f5f5f5",
  yellow: "#ffff00",
  yellowgreen: "#9acd32"
}, Ay = /^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/, Vy = /^#?([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$/, dh = (e) => {
  if (e.match(Ay)) {
    (e.length === 4 || e.length === 7) && (e = e.substr(1)), e.length === 3 && (e = e.split(""), e = e[0] + e[0] + e[1] + e[1] + e[2] + e[2]);
    const t = parseInt(e, 16), n = t >> 16, s = t >> 8 & 255, i = t & 255;
    return [n, s, i, 1];
  }
  if (e.match(Vy)) {
    (e.length === 5 || e.length === 9) && (e = e.substr(1)), e.length === 4 && (e = e.split(""), e = e[0] + e[0] + e[1] + e[1] + e[2] + e[2] + e[3] + e[3]);
    const t = parseInt(e, 16), n = t >> 24 & 255, s = t >> 16 & 255, i = t >> 8 & 255, o = Math.round((t & 255) / 255 * 100) / 100;
    return [n, s, i, o];
  }
  throw new Error(`unknown hex color: ${e}`);
}, { round: _i } = Math, ph = (...e) => {
  let [t, n, s, i] = Q(e, "rgba"), o = es(e) || "auto";
  i === void 0 && (i = 1), o === "auto" && (o = i < 1 ? "rgba" : "rgb"), t = _i(t), n = _i(n), s = _i(s);
  let a = "000000" + (t << 16 | n << 8 | s).toString(16);
  a = a.substr(a.length - 6);
  let l = "0" + _i(i * 255).toString(16);
  switch (l = l.substr(l.length - 2), o.toLowerCase()) {
    case "rgba":
      return `#${a}${l}`;
    case "argb":
      return `#${l}${a}`;
    default:
      return `#${a}`;
  }
};
V.prototype.name = function() {
  const e = ph(this._rgb, "rgb");
  for (let t of Object.keys(Gn))
    if (Gn[t] === e) return t.toLowerCase();
  return e;
};
J.format.named = (e) => {
  if (e = e.toLowerCase(), Gn[e]) return dh(Gn[e]);
  throw new Error("unknown color name: " + e);
};
J.autodetect.push({
  p: 5,
  test: (e, ...t) => {
    if (!t.length && nt(e) === "string" && Gn[e.toLowerCase()])
      return "named";
  }
});
V.prototype.alpha = function(e, t = !1) {
  return e !== void 0 && nt(e) === "number" ? t ? (this._rgb[3] = e, this) : new V([this._rgb[0], this._rgb[1], this._rgb[2], e], "rgb") : this._rgb[3];
};
V.prototype.clipped = function() {
  return this._rgb._clipped || !1;
};
const Te = {
  // Corresponds roughly to RGB brighter/darker
  Kn: 18,
  // D65 standard referent
  labWhitePoint: "d65",
  Xn: 0.95047,
  Yn: 1,
  Zn: 1.08883,
  kE: 216 / 24389,
  kKE: 8,
  kK: 24389 / 27,
  RefWhiteRGB: {
    // sRGB
    X: 0.95047,
    Y: 1,
    Z: 1.08883
  },
  MtxRGB2XYZ: {
    m00: 0.4124564390896922,
    m01: 0.21267285140562253,
    m02: 0.0193338955823293,
    m10: 0.357576077643909,
    m11: 0.715152155287818,
    m12: 0.11919202588130297,
    m20: 0.18043748326639894,
    m21: 0.07217499330655958,
    m22: 0.9503040785363679
  },
  MtxXYZ2RGB: {
    m00: 3.2404541621141045,
    m01: -0.9692660305051868,
    m02: 0.055643430959114726,
    m10: -1.5371385127977166,
    m11: 1.8760108454466942,
    m12: -0.2040259135167538,
    m20: -0.498531409556016,
    m21: 0.041556017530349834,
    m22: 1.0572251882231791
  },
  // used in rgb2xyz
  As: 0.9414285350000001,
  Bs: 1.040417467,
  Cs: 1.089532651,
  MtxAdaptMa: {
    m00: 0.8951,
    m01: -0.7502,
    m02: 0.0389,
    m10: 0.2664,
    m11: 1.7135,
    m12: -0.0685,
    m20: -0.1614,
    m21: 0.0367,
    m22: 1.0296
  },
  MtxAdaptMaI: {
    m00: 0.9869929054667123,
    m01: 0.43230526972339456,
    m02: -0.008528664575177328,
    m10: -0.14705425642099013,
    m11: 0.5183602715367776,
    m12: 0.04004282165408487,
    m20: 0.15996265166373125,
    m21: 0.0492912282128556,
    m22: 0.9684866957875502
  }
}, Ry = /* @__PURE__ */ new Map([
  // ASTM E308-01
  ["a", [1.0985, 0.35585]],
  // Wyszecki & Stiles, p. 769
  ["b", [1.0985, 0.35585]],
  // C ASTM E308-01
  ["c", [0.98074, 1.18232]],
  // D50 (ASTM E308-01)
  ["d50", [0.96422, 0.82521]],
  // D55 (ASTM E308-01)
  ["d55", [0.95682, 0.92149]],
  // D65 (ASTM E308-01)
  ["d65", [0.95047, 1.08883]],
  // E (ASTM E308-01)
  ["e", [1, 1, 1]],
  // F2 (ASTM E308-01)
  ["f2", [0.99186, 0.67393]],
  // F7 (ASTM E308-01)
  ["f7", [0.95041, 1.08747]],
  // F11 (ASTM E308-01)
  ["f11", [1.00962, 0.6435]],
  ["icc", [0.96422, 0.82521]]
]);
function We(e) {
  const t = Ry.get(String(e).toLowerCase());
  if (!t)
    throw new Error("unknown Lab illuminant " + e);
  Te.labWhitePoint = e, Te.Xn = t[0], Te.Zn = t[1];
}
function Ws() {
  return Te.labWhitePoint;
}
const Oa = (...e) => {
  e = Q(e, "lab");
  const [t, n, s] = e, [i, o, r] = Iy(t, n, s), [a, l, c] = gh(i, o, r);
  return [a, l, c, e.length > 3 ? e[3] : 1];
}, Iy = (e, t, n) => {
  const { kE: s, kK: i, kKE: o, Xn: r, Yn: a, Zn: l } = Te, c = (e + 16) / 116, f = 2e-3 * t + c, u = c - 5e-3 * n, h = f * f * f, d = u * u * u, p = h > s ? h : (116 * f - 16) / i, g = e > o ? Math.pow((e + 16) / 116, 3) : e / i, b = d > s ? d : (116 * u - 16) / i, y = p * r, O = g * a, M = b * l;
  return [y, O, M];
}, Jo = (e) => {
  const t = Math.sign(e);
  return e = Math.abs(e), (e <= 31308e-7 ? e * 12.92 : 1.055 * Math.pow(e, 1 / 2.4) - 0.055) * t;
}, gh = (e, t, n) => {
  const { MtxAdaptMa: s, MtxAdaptMaI: i, MtxXYZ2RGB: o, RefWhiteRGB: r, Xn: a, Yn: l, Zn: c } = Te, f = a * s.m00 + l * s.m10 + c * s.m20, u = a * s.m01 + l * s.m11 + c * s.m21, h = a * s.m02 + l * s.m12 + c * s.m22, d = r.X * s.m00 + r.Y * s.m10 + r.Z * s.m20, p = r.X * s.m01 + r.Y * s.m11 + r.Z * s.m21, g = r.X * s.m02 + r.Y * s.m12 + r.Z * s.m22, b = (e * s.m00 + t * s.m10 + n * s.m20) * (d / f), y = (e * s.m01 + t * s.m11 + n * s.m21) * (p / u), O = (e * s.m02 + t * s.m12 + n * s.m22) * (g / h), M = b * i.m00 + y * i.m10 + O * i.m20, P = b * i.m01 + y * i.m11 + O * i.m21, w = b * i.m02 + y * i.m12 + O * i.m22, k = Jo(
    M * o.m00 + P * o.m10 + w * o.m20
  ), v = Jo(
    M * o.m01 + P * o.m11 + w * o.m21
  ), S = Jo(
    M * o.m02 + P * o.m12 + w * o.m22
  );
  return [k * 255, v * 255, S * 255];
}, Sa = (...e) => {
  const [t, n, s, ...i] = Q(e, "rgb"), [o, r, a] = mh(t, n, s), [l, c, f] = Ly(o, r, a);
  return [l, c, f, ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
};
function Ly(e, t, n) {
  const { Xn: s, Yn: i, Zn: o, kE: r, kK: a } = Te, l = e / s, c = t / i, f = n / o, u = l > r ? Math.pow(l, 1 / 3) : (a * l + 16) / 116, h = c > r ? Math.pow(c, 1 / 3) : (a * c + 16) / 116, d = f > r ? Math.pow(f, 1 / 3) : (a * f + 16) / 116;
  return [116 * h - 16, 500 * (u - h), 200 * (h - d)];
}
function Qo(e) {
  const t = Math.sign(e);
  return e = Math.abs(e), (e <= 0.04045 ? e / 12.92 : Math.pow((e + 0.055) / 1.055, 2.4)) * t;
}
const mh = (e, t, n) => {
  e = Qo(e / 255), t = Qo(t / 255), n = Qo(n / 255);
  const { MtxRGB2XYZ: s, MtxAdaptMa: i, MtxAdaptMaI: o, Xn: r, Yn: a, Zn: l, As: c, Bs: f, Cs: u } = Te;
  let h = e * s.m00 + t * s.m10 + n * s.m20, d = e * s.m01 + t * s.m11 + n * s.m21, p = e * s.m02 + t * s.m12 + n * s.m22;
  const g = r * i.m00 + a * i.m10 + l * i.m20, b = r * i.m01 + a * i.m11 + l * i.m21, y = r * i.m02 + a * i.m12 + l * i.m22;
  let O = h * i.m00 + d * i.m10 + p * i.m20, M = h * i.m01 + d * i.m11 + p * i.m21, P = h * i.m02 + d * i.m12 + p * i.m22;
  return O *= g / c, M *= b / f, P *= y / u, h = O * o.m00 + M * o.m10 + P * o.m20, d = O * o.m01 + M * o.m11 + P * o.m21, p = O * o.m02 + M * o.m12 + P * o.m22, [h, d, p];
};
V.prototype.lab = function() {
  return Sa(this._rgb);
};
const Fy = (...e) => new V(...e, "lab");
Object.assign(q, { lab: Fy, getLabWhitePoint: Ws, setLabWhitePoint: We });
J.format.lab = Oa;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "lab"), nt(e) === "array" && e.length === 3)
      return "lab";
  }
});
V.prototype.darken = function(e = 1) {
  const t = this, n = t.lab();
  return n[0] -= Te.Kn * e, new V(n, "lab").alpha(t.alpha(), !0);
};
V.prototype.brighten = function(e = 1) {
  return this.darken(-e);
};
V.prototype.darker = V.prototype.darken;
V.prototype.brighter = V.prototype.brighten;
V.prototype.get = function(e) {
  const [t, n] = e.split("."), s = this[t]();
  if (n) {
    const i = t.indexOf(n) - (t.substr(0, 2) === "ok" ? 2 : 0);
    if (i > -1) return s[i];
    throw new Error(`unknown channel ${n} in mode ${t}`);
  } else
    return s;
};
const { pow: $y } = Math, By = 1e-7, jy = 20;
V.prototype.luminance = function(e, t = "rgb") {
  if (e !== void 0 && nt(e) === "number") {
    if (e === 0)
      return new V([0, 0, 0, this._rgb[3]], "rgb");
    if (e === 1)
      return new V([255, 255, 255, this._rgb[3]], "rgb");
    let n = this.luminance(), s = jy;
    const i = (r, a) => {
      const l = r.interpolate(a, 0.5, t), c = l.luminance();
      return Math.abs(e - c) < By || !s-- ? l : c > e ? i(r, l) : i(l, a);
    }, o = (n > e ? i(new V([0, 0, 0]), this) : i(this, new V([255, 255, 255]))).rgb();
    return new V([...o, this._rgb[3]]);
  }
  return zy(...this._rgb.slice(0, 3));
};
const zy = (e, t, n) => (e = tr(e), t = tr(t), n = tr(n), 0.2126 * e + 0.7152 * t + 0.0722 * n), tr = (e) => (e /= 255, e <= 0.03928 ? e / 12.92 : $y((e + 0.055) / 1.055, 2.4)), At = {}, Zn = (e, t, n = 0.5, ...s) => {
  let i = s[0] || "lrgb";
  if (!At[i] && !s.length && (i = Object.keys(At)[0]), !At[i])
    throw new Error(`interpolation mode ${i} is not defined`);
  return nt(e) !== "object" && (e = new V(e)), nt(t) !== "object" && (t = new V(t)), At[i](e, t, n).alpha(
    e.alpha() + n * (t.alpha() - e.alpha())
  );
};
V.prototype.mix = V.prototype.interpolate = function(e, t = 0.5, ...n) {
  return Zn(this, e, t, ...n);
};
V.prototype.premultiply = function(e = !1) {
  const t = this._rgb, n = t[3];
  return e ? (this._rgb = [t[0] * n, t[1] * n, t[2] * n, n], this) : new V([t[0] * n, t[1] * n, t[2] * n, n], "rgb");
};
const { sin: Hy, cos: Wy } = Math, bh = (...e) => {
  let [t, n, s] = Q(e, "lch");
  return isNaN(s) && (s = 0), s = s * Cy, [t, Wy(s) * n, Hy(s) * n];
}, Ma = (...e) => {
  e = Q(e, "lch");
  const [t, n, s] = e, [i, o, r] = bh(t, n, s), [a, l, c] = Oa(i, o, r);
  return [a, l, c, e.length > 3 ? e[3] : 1];
}, Uy = (...e) => {
  const t = hh(Q(e, "hcl"));
  return Ma(...t);
}, { sqrt: Yy, atan2: Ky, round: qy } = Math, _h = (...e) => {
  const [t, n, s] = Q(e, "lab"), i = Yy(n * n + s * s);
  let o = (Ky(s, n) * Py + 360) % 360;
  return qy(i * 1e4) === 0 && (o = Number.NaN), [t, i, o];
}, ka = (...e) => {
  const [t, n, s, ...i] = Q(e, "rgb"), [o, r, a] = Sa(t, n, s), [l, c, f] = _h(o, r, a);
  return [l, c, f, ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
};
V.prototype.lch = function() {
  return ka(this._rgb);
};
V.prototype.hcl = function() {
  return hh(ka(this._rgb));
};
const Xy = (...e) => new V(...e, "lch"), Gy = (...e) => new V(...e, "hcl");
Object.assign(q, { lch: Xy, hcl: Gy });
J.format.lch = Ma;
J.format.hcl = Uy;
["lch", "hcl"].forEach(
  (e) => J.autodetect.push({
    p: 2,
    test: (...t) => {
      if (t = Q(t, e), nt(t) === "array" && t.length === 3)
        return e;
    }
  })
);
V.prototype.saturate = function(e = 1) {
  const t = this, n = t.lch();
  return n[1] += Te.Kn * e, n[1] < 0 && (n[1] = 0), new V(n, "lch").alpha(t.alpha(), !0);
};
V.prototype.desaturate = function(e = 1) {
  return this.saturate(-e);
};
V.prototype.set = function(e, t, n = !1) {
  const [s, i] = e.split("."), o = this[s]();
  if (i) {
    const r = s.indexOf(i) - (s.substr(0, 2) === "ok" ? 2 : 0);
    if (r > -1) {
      if (nt(t) == "string")
        switch (t.charAt(0)) {
          case "+":
            o[r] += +t;
            break;
          case "-":
            o[r] += +t;
            break;
          case "*":
            o[r] *= +t.substr(1);
            break;
          case "/":
            o[r] /= +t.substr(1);
            break;
          default:
            o[r] = +t;
        }
      else if (nt(t) === "number")
        o[r] = t;
      else
        throw new Error("unsupported value for Color.set");
      const a = new V(o, s);
      return n ? (this._rgb = a._rgb, this) : a;
    }
    throw new Error(`unknown channel ${i} in mode ${s}`);
  } else
    return o;
};
V.prototype.tint = function(e = 0.5, ...t) {
  return Zn(this, "white", e, ...t);
};
V.prototype.shade = function(e = 0.5, ...t) {
  return Zn(this, "black", e, ...t);
};
const Zy = (e, t, n) => {
  const s = e._rgb, i = t._rgb;
  return new V(
    s[0] + n * (i[0] - s[0]),
    s[1] + n * (i[1] - s[1]),
    s[2] + n * (i[2] - s[2]),
    "rgb"
  );
};
At.rgb = Zy;
const { sqrt: er, pow: Bn } = Math, Jy = (e, t, n) => {
  const [s, i, o] = e._rgb, [r, a, l] = t._rgb;
  return new V(
    er(Bn(s, 2) * (1 - n) + Bn(r, 2) * n),
    er(Bn(i, 2) * (1 - n) + Bn(a, 2) * n),
    er(Bn(o, 2) * (1 - n) + Bn(l, 2) * n),
    "rgb"
  );
};
At.lrgb = Jy;
const Qy = (e, t, n) => {
  const s = e.lab(), i = t.lab();
  return new V(
    s[0] + n * (i[0] - s[0]),
    s[1] + n * (i[1] - s[1]),
    s[2] + n * (i[2] - s[2]),
    "lab"
  );
};
At.lab = Qy;
const ns = (e, t, n, s) => {
  let i, o;
  s === "hsl" ? (i = e.hsl(), o = t.hsl()) : s === "hsv" ? (i = e.hsv(), o = t.hsv()) : s === "hcg" ? (i = e.hcg(), o = t.hcg()) : s === "hsi" ? (i = e.hsi(), o = t.hsi()) : s === "lch" || s === "hcl" ? (s = "hcl", i = e.hcl(), o = t.hcl()) : s === "oklch" && (i = e.oklch().reverse(), o = t.oklch().reverse());
  let r, a, l, c, f, u;
  (s.substr(0, 1) === "h" || s === "oklch") && ([r, l, f] = i, [a, c, u] = o);
  let h, d, p, g;
  return !isNaN(r) && !isNaN(a) ? (a > r && a - r > 180 ? g = a - (r + 360) : a < r && r - a > 180 ? g = a + 360 - r : g = a - r, d = r + n * g) : isNaN(r) ? isNaN(a) ? d = Number.NaN : (d = a, (f == 1 || f == 0) && s != "hsv" && (h = c)) : (d = r, (u == 1 || u == 0) && s != "hsv" && (h = l)), h === void 0 && (h = l + n * (c - l)), p = f + n * (u - f), s === "oklch" ? new V([p, h, d], s) : new V([d, h, p], s);
}, yh = (e, t, n) => ns(e, t, n, "lch");
At.lch = yh;
At.hcl = yh;
const t1 = (e) => {
  if (nt(e) == "number" && e >= 0 && e <= 16777215) {
    const t = e >> 16, n = e >> 8 & 255, s = e & 255;
    return [t, n, s, 1];
  }
  throw new Error("unknown num color: " + e);
}, e1 = (...e) => {
  const [t, n, s] = Q(e, "rgb");
  return (t << 16) + (n << 8) + s;
};
V.prototype.num = function() {
  return e1(this._rgb);
};
const n1 = (...e) => new V(...e, "num");
Object.assign(q, { num: n1 });
J.format.num = t1;
J.autodetect.push({
  p: 5,
  test: (...e) => {
    if (e.length === 1 && nt(e[0]) === "number" && e[0] >= 0 && e[0] <= 16777215)
      return "num";
  }
});
const s1 = (e, t, n) => {
  const s = e.num(), i = t.num();
  return new V(s + n * (i - s), "num");
};
At.num = s1;
const { floor: i1 } = Math, o1 = (...e) => {
  e = Q(e, "hcg");
  let [t, n, s] = e, i, o, r;
  s = s * 255;
  const a = n * 255;
  if (n === 0)
    i = o = r = s;
  else {
    t === 360 && (t = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 60;
    const l = i1(t), c = t - l, f = s * (1 - n), u = f + a * (1 - c), h = f + a * c, d = f + a;
    switch (l) {
      case 0:
        [i, o, r] = [d, h, f];
        break;
      case 1:
        [i, o, r] = [u, d, f];
        break;
      case 2:
        [i, o, r] = [f, d, h];
        break;
      case 3:
        [i, o, r] = [f, u, d];
        break;
      case 4:
        [i, o, r] = [h, f, d];
        break;
      case 5:
        [i, o, r] = [d, f, u];
        break;
    }
  }
  return [i, o, r, e.length > 3 ? e[3] : 1];
}, r1 = (...e) => {
  const [t, n, s] = Q(e, "rgb"), i = fh(t, n, s), o = uh(t, n, s), r = o - i, a = r * 100 / 255, l = i / (255 - r) * 100;
  let c;
  return r === 0 ? c = Number.NaN : (t === o && (c = (n - s) / r), n === o && (c = 2 + (s - t) / r), s === o && (c = 4 + (t - n) / r), c *= 60, c < 0 && (c += 360)), [c, a, l];
};
V.prototype.hcg = function() {
  return r1(this._rgb);
};
const a1 = (...e) => new V(...e, "hcg");
q.hcg = a1;
J.format.hcg = o1;
J.autodetect.push({
  p: 1,
  test: (...e) => {
    if (e = Q(e, "hcg"), nt(e) === "array" && e.length === 3)
      return "hcg";
  }
});
const l1 = (e, t, n) => ns(e, t, n, "hcg");
At.hcg = l1;
const { cos: jn } = Math, c1 = (...e) => {
  e = Q(e, "hsi");
  let [t, n, s] = e, i, o, r;
  return isNaN(t) && (t = 0), isNaN(n) && (n = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 360, t < 1 / 3 ? (r = (1 - n) / 3, i = (1 + n * jn(He * t) / jn(Zo - He * t)) / 3, o = 1 - (r + i)) : t < 2 / 3 ? (t -= 1 / 3, i = (1 - n) / 3, o = (1 + n * jn(He * t) / jn(Zo - He * t)) / 3, r = 1 - (i + o)) : (t -= 2 / 3, o = (1 - n) / 3, r = (1 + n * jn(He * t) / jn(Zo - He * t)) / 3, i = 1 - (o + r)), i = Pn(s * i * 3), o = Pn(s * o * 3), r = Pn(s * r * 3), [i * 255, o * 255, r * 255, e.length > 3 ? e[3] : 1];
}, { min: f1, sqrt: u1, acos: h1 } = Math, d1 = (...e) => {
  let [t, n, s] = Q(e, "rgb");
  t /= 255, n /= 255, s /= 255;
  let i;
  const o = f1(t, n, s), r = (t + n + s) / 3, a = r > 0 ? 1 - o / r : 0;
  return a === 0 ? i = NaN : (i = (t - n + (t - s)) / 2, i /= u1((t - n) * (t - n) + (t - s) * (n - s)), i = h1(i), s > n && (i = He - i), i /= He), [i * 360, a, r];
};
V.prototype.hsi = function() {
  return d1(this._rgb);
};
const p1 = (...e) => new V(...e, "hsi");
q.hsi = p1;
J.format.hsi = c1;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "hsi"), nt(e) === "array" && e.length === 3)
      return "hsi";
  }
});
const g1 = (e, t, n) => ns(e, t, n, "hsi");
At.hsi = g1;
const $r = (...e) => {
  e = Q(e, "hsl");
  const [t, n, s] = e;
  let i, o, r;
  if (n === 0)
    i = o = r = s * 255;
  else {
    const a = [0, 0, 0], l = [0, 0, 0], c = s < 0.5 ? s * (1 + n) : s + n - s * n, f = 2 * s - c, u = t / 360;
    a[0] = u + 1 / 3, a[1] = u, a[2] = u - 1 / 3;
    for (let h = 0; h < 3; h++)
      a[h] < 0 && (a[h] += 1), a[h] > 1 && (a[h] -= 1), 6 * a[h] < 1 ? l[h] = f + (c - f) * 6 * a[h] : 2 * a[h] < 1 ? l[h] = c : 3 * a[h] < 2 ? l[h] = f + (c - f) * (2 / 3 - a[h]) * 6 : l[h] = f;
    [i, o, r] = [l[0] * 255, l[1] * 255, l[2] * 255];
  }
  return e.length > 3 ? [i, o, r, e[3]] : [i, o, r, 1];
}, xh = (...e) => {
  e = Q(e, "rgba");
  let [t, n, s] = e;
  t /= 255, n /= 255, s /= 255;
  const i = fh(t, n, s), o = uh(t, n, s), r = (o + i) / 2;
  let a, l;
  return o === i ? (a = 0, l = Number.NaN) : a = r < 0.5 ? (o - i) / (o + i) : (o - i) / (2 - o - i), t == o ? l = (n - s) / (o - i) : n == o ? l = 2 + (s - t) / (o - i) : s == o && (l = 4 + (t - n) / (o - i)), l *= 60, l < 0 && (l += 360), e.length > 3 && e[3] !== void 0 ? [l, a, r, e[3]] : [l, a, r];
};
V.prototype.hsl = function() {
  return xh(this._rgb);
};
const m1 = (...e) => new V(...e, "hsl");
q.hsl = m1;
J.format.hsl = $r;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "hsl"), nt(e) === "array" && e.length === 3)
      return "hsl";
  }
});
const b1 = (e, t, n) => ns(e, t, n, "hsl");
At.hsl = b1;
const { floor: _1 } = Math, y1 = (...e) => {
  e = Q(e, "hsv");
  let [t, n, s] = e, i, o, r;
  if (s *= 255, n === 0)
    i = o = r = s;
  else {
    t === 360 && (t = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 60;
    const a = _1(t), l = t - a, c = s * (1 - n), f = s * (1 - n * l), u = s * (1 - n * (1 - l));
    switch (a) {
      case 0:
        [i, o, r] = [s, u, c];
        break;
      case 1:
        [i, o, r] = [f, s, c];
        break;
      case 2:
        [i, o, r] = [c, s, u];
        break;
      case 3:
        [i, o, r] = [c, f, s];
        break;
      case 4:
        [i, o, r] = [u, c, s];
        break;
      case 5:
        [i, o, r] = [s, c, f];
        break;
    }
  }
  return [i, o, r, e.length > 3 ? e[3] : 1];
}, { min: x1, max: v1 } = Math, w1 = (...e) => {
  e = Q(e, "rgb");
  let [t, n, s] = e;
  const i = x1(t, n, s), o = v1(t, n, s), r = o - i;
  let a, l, c;
  return c = o / 255, o === 0 ? (a = Number.NaN, l = 0) : (l = r / o, t === o && (a = (n - s) / r), n === o && (a = 2 + (s - t) / r), s === o && (a = 4 + (t - n) / r), a *= 60, a < 0 && (a += 360)), [a, l, c];
};
V.prototype.hsv = function() {
  return w1(this._rgb);
};
const E1 = (...e) => new V(...e, "hsv");
q.hsv = E1;
J.format.hsv = y1;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "hsv"), nt(e) === "array" && e.length === 3)
      return "hsv";
  }
});
const O1 = (e, t, n) => ns(e, t, n, "hsv");
At.hsv = O1;
function no(e, t) {
  let n = e.length;
  Array.isArray(e[0]) || (e = [e]), Array.isArray(t[0]) || (t = t.map((r) => [r]));
  let s = t[0].length, i = t[0].map((r, a) => t.map((l) => l[a])), o = e.map(
    (r) => i.map((a) => Array.isArray(r) ? r.reduce((l, c, f) => l + c * (a[f] || 0), 0) : a.reduce((l, c) => l + c * r, 0))
  );
  return n === 1 && (o = o[0]), s === 1 ? o.map((r) => r[0]) : o;
}
const Na = (...e) => {
  e = Q(e, "lab");
  const [t, n, s, ...i] = e, [o, r, a] = S1([t, n, s]), [l, c, f] = gh(o, r, a);
  return [l, c, f, ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
};
function S1(e) {
  var t = [
    [1.2268798758459243, -0.5578149944602171, 0.2813910456659647],
    [-0.0405757452148008, 1.112286803280317, -0.0717110580655164],
    [-0.0763729366746601, -0.4214933324022432, 1.5869240198367816]
  ], n = [
    [1, 0.3963377773761749, 0.2158037573099136],
    [1, -0.1055613458156586, -0.0638541728258133],
    [1, -0.0894841775298119, -1.2914855480194092]
  ], s = no(n, e);
  return no(
    t,
    s.map((i) => i ** 3)
  );
}
const Da = (...e) => {
  const [t, n, s, ...i] = Q(e, "rgb"), o = mh(t, n, s);
  return [...M1(o), ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
};
function M1(e) {
  const t = [
    [0.819022437996703, 0.3619062600528904, -0.1288737815209879],
    [0.0329836539323885, 0.9292868615863434, 0.0361446663506424],
    [0.0481771893596242, 0.2642395317527308, 0.6335478284694309]
  ], n = [
    [0.210454268309314, 0.7936177747023054, -0.0040720430116193],
    [1.9779985324311684, -2.42859224204858, 0.450593709617411],
    [0.0259040424655478, 0.7827717124575296, -0.8086757549230774]
  ], s = no(t, e);
  return no(
    n,
    s.map((i) => Math.cbrt(i))
  );
}
V.prototype.oklab = function() {
  return Da(this._rgb);
};
const k1 = (...e) => new V(...e, "oklab");
Object.assign(q, { oklab: k1 });
J.format.oklab = Na;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "oklab"), nt(e) === "array" && e.length === 3)
      return "oklab";
  }
});
const N1 = (e, t, n) => {
  const s = e.oklab(), i = t.oklab();
  return new V(
    s[0] + n * (i[0] - s[0]),
    s[1] + n * (i[1] - s[1]),
    s[2] + n * (i[2] - s[2]),
    "oklab"
  );
};
At.oklab = N1;
const D1 = (e, t, n) => ns(e, t, n, "oklch");
At.oklch = D1;
const { pow: nr, sqrt: sr, PI: ir, cos: Bc, sin: jc, atan2: C1 } = Math, P1 = (e, t = "lrgb", n = null) => {
  const s = e.length;
  n || (n = Array.from(new Array(s)).map(() => 1));
  const i = s / n.reduce(function(u, h) {
    return u + h;
  });
  if (n.forEach((u, h) => {
    n[h] *= i;
  }), e = e.map((u) => new V(u)), t === "lrgb")
    return T1(e, n);
  const o = e.shift(), r = o.get(t), a = [];
  let l = 0, c = 0;
  for (let u = 0; u < r.length; u++)
    if (r[u] = (r[u] || 0) * n[0], a.push(isNaN(r[u]) ? 0 : n[0]), t.charAt(u) === "h" && !isNaN(r[u])) {
      const h = r[u] / 180 * ir;
      l += Bc(h) * n[0], c += jc(h) * n[0];
    }
  let f = o.alpha() * n[0];
  e.forEach((u, h) => {
    const d = u.get(t);
    f += u.alpha() * n[h + 1];
    for (let p = 0; p < r.length; p++)
      if (!isNaN(d[p]))
        if (a[p] += n[h + 1], t.charAt(p) === "h") {
          const g = d[p] / 180 * ir;
          l += Bc(g) * n[h + 1], c += jc(g) * n[h + 1];
        } else
          r[p] += d[p] * n[h + 1];
  });
  for (let u = 0; u < r.length; u++)
    if (t.charAt(u) === "h") {
      let h = C1(c / a[u], l / a[u]) / ir * 180;
      for (; h < 0; ) h += 360;
      for (; h >= 360; ) h -= 360;
      r[u] = h;
    } else
      r[u] = r[u] / a[u];
  return f /= s, new V(r, t).alpha(f > 0.99999 ? 1 : f, !0);
}, T1 = (e, t) => {
  const n = e.length, s = [0, 0, 0, 0];
  for (let i = 0; i < e.length; i++) {
    const o = e[i], r = t[i] / n, a = o._rgb;
    s[0] += nr(a[0], 2) * r, s[1] += nr(a[1], 2) * r, s[2] += nr(a[2], 2) * r, s[3] += a[3] * r;
  }
  return s[0] = sr(s[0]), s[1] = sr(s[1]), s[2] = sr(s[2]), s[3] > 0.9999999 && (s[3] = 1), new V(Ea(s));
}, { pow: A1 } = Math;
function so(e) {
  let t = "rgb", n = q("#ccc"), s = 0, i = [0, 1], o = [], r = [0, 0], a = !1, l = [], c = !1, f = 0, u = 1, h = !1, d = {}, p = !0, g = 1;
  const b = function(v) {
    if (v = v || ["#fff", "#000"], v && nt(v) === "string" && q.brewer && q.brewer[v.toLowerCase()] && (v = q.brewer[v.toLowerCase()]), nt(v) === "array") {
      v.length === 1 && (v = [v[0], v[0]]), v = v.slice(0);
      for (let S = 0; S < v.length; S++)
        v[S] = q(v[S]);
      o.length = 0;
      for (let S = 0; S < v.length; S++)
        o.push(S / (v.length - 1));
    }
    return w(), l = v;
  }, y = function(v) {
    if (a != null) {
      const S = a.length - 1;
      let D = 0;
      for (; D < S && v >= a[D]; )
        D++;
      return D - 1;
    }
    return 0;
  };
  let O = (v) => v, M = (v) => v;
  const P = function(v, S) {
    let D, F;
    if (S == null && (S = !1), isNaN(v) || v === null)
      return n;
    S ? F = v : a && a.length > 2 ? F = y(v) / (a.length - 2) : u !== f ? F = (v - f) / (u - f) : F = 1, F = M(F), S || (F = O(F)), g !== 1 && (F = A1(F, g)), F = r[0] + F * (1 - r[0] - r[1]), F = Pn(F, 0, 1);
    const z = Math.floor(F * 1e4);
    if (p && d[z])
      D = d[z];
    else {
      if (nt(l) === "array")
        for (let j = 0; j < o.length; j++) {
          const tt = o[j];
          if (F <= tt) {
            D = l[j];
            break;
          }
          if (F >= tt && j === o.length - 1) {
            D = l[j];
            break;
          }
          if (F > tt && F < o[j + 1]) {
            F = (F - tt) / (o[j + 1] - tt), D = q.interpolate(
              l[j],
              l[j + 1],
              F,
              t
            );
            break;
          }
        }
      else nt(l) === "function" && (D = l(F));
      p && (d[z] = D);
    }
    return D;
  };
  var w = () => d = {};
  b(e);
  const k = function(v) {
    const S = q(P(v));
    return c && S[c] ? S[c]() : S;
  };
  return k.classes = function(v) {
    if (v != null) {
      if (nt(v) === "array")
        a = v, i = [v[0], v[v.length - 1]];
      else {
        const S = q.analyze(i);
        v === 0 ? a = [S.min, S.max] : a = q.limits(S, "e", v);
      }
      return k;
    }
    return a;
  }, k.domain = function(v) {
    if (!arguments.length)
      return i;
    f = v[0], u = v[v.length - 1], o = [];
    const S = l.length;
    if (v.length === S && f !== u)
      for (let D of Array.from(v))
        o.push((D - f) / (u - f));
    else {
      for (let D = 0; D < S; D++)
        o.push(D / (S - 1));
      if (v.length > 2) {
        const D = v.map((z, j) => j / (v.length - 1)), F = v.map((z) => (z - f) / (u - f));
        F.every((z, j) => D[j] === z) || (M = (z) => {
          if (z <= 0 || z >= 1) return z;
          let j = 0;
          for (; z >= F[j + 1]; ) j++;
          const tt = (z - F[j]) / (F[j + 1] - F[j]);
          return D[j] + tt * (D[j + 1] - D[j]);
        });
      }
    }
    return i = [f, u], k;
  }, k.mode = function(v) {
    return arguments.length ? (t = v, w(), k) : t;
  }, k.range = function(v, S) {
    return b(v), k;
  }, k.out = function(v) {
    return c = v, k;
  }, k.spread = function(v) {
    return arguments.length ? (s = v, k) : s;
  }, k.correctLightness = function(v) {
    return v == null && (v = !0), h = v, w(), h ? O = function(S) {
      const D = P(0, !0).lab()[0], F = P(1, !0).lab()[0], z = D > F;
      let j = P(S, !0).lab()[0];
      const tt = D + (F - D) * S;
      let Et = j - tt, it = 0, st = 1, W = 20;
      for (; Math.abs(Et) > 0.01 && W-- > 0; )
        (function() {
          return z && (Et *= -1), Et < 0 ? (it = S, S += (st - S) * 0.5) : (st = S, S += (it - S) * 0.5), j = P(S, !0).lab()[0], Et = j - tt;
        })();
      return S;
    } : O = (S) => S, k;
  }, k.padding = function(v) {
    return v != null ? (nt(v) === "number" && (v = [v, v]), r = v, k) : r;
  }, k.colors = function(v, S) {
    arguments.length < 2 && (S = "hex");
    let D = [];
    if (arguments.length === 0)
      D = l.slice(0);
    else if (v === 1)
      D = [k(0.5)];
    else if (v > 1) {
      const F = i[0], z = i[1] - F;
      D = V1(0, v).map(
        (j) => k(F + j / (v - 1) * z)
      );
    } else {
      e = [];
      let F = [];
      if (a && a.length > 2)
        for (let z = 1, j = a.length, tt = 1 <= j; tt ? z < j : z > j; tt ? z++ : z--)
          F.push((a[z - 1] + a[z]) * 0.5);
      else
        F = i;
      D = F.map((z) => k(z));
    }
    return q[S] && (D = D.map((F) => F[S]())), D;
  }, k.cache = function(v) {
    return v != null ? (p = v, k) : p;
  }, k.gamma = function(v) {
    return v != null ? (g = v, k) : g;
  }, k.nodata = function(v) {
    return v != null ? (n = q(v), k) : n;
  }, k;
}
function V1(e, t, n) {
  let s = [], i = e < t, o = t;
  for (let r = e; i ? r < o : r > o; i ? r++ : r--)
    s.push(r);
  return s;
}
const R1 = function(e) {
  let t = [1, 1];
  for (let n = 1; n < e; n++) {
    let s = [1];
    for (let i = 1; i <= t.length; i++)
      s[i] = (t[i] || 0) + t[i - 1];
    t = s;
  }
  return t;
}, I1 = function(e) {
  let t, n, s, i;
  if (e = e.map((o) => new V(o)), e.length === 2)
    [n, s] = e.map((o) => o.lab()), t = function(o) {
      const r = [0, 1, 2].map((a) => n[a] + o * (s[a] - n[a]));
      return new V(r, "lab");
    };
  else if (e.length === 3)
    [n, s, i] = e.map((o) => o.lab()), t = function(o) {
      const r = [0, 1, 2].map(
        (a) => (1 - o) * (1 - o) * n[a] + 2 * (1 - o) * o * s[a] + o * o * i[a]
      );
      return new V(r, "lab");
    };
  else if (e.length === 4) {
    let o;
    [n, s, i, o] = e.map((r) => r.lab()), t = function(r) {
      const a = [0, 1, 2].map(
        (l) => (1 - r) * (1 - r) * (1 - r) * n[l] + 3 * (1 - r) * (1 - r) * r * s[l] + 3 * (1 - r) * r * r * i[l] + r * r * r * o[l]
      );
      return new V(a, "lab");
    };
  } else if (e.length >= 5) {
    let o, r, a;
    o = e.map((l) => l.lab()), a = e.length - 1, r = R1(a), t = function(l) {
      const c = 1 - l, f = [0, 1, 2].map(
        (u) => o.reduce(
          (h, d, p) => h + r[p] * c ** (a - p) * l ** p * d[u],
          0
        )
      );
      return new V(f, "lab");
    };
  } else
    throw new RangeError("No point in running bezier with only one color.");
  return t;
}, L1 = (e) => {
  const t = I1(e);
  return t.scale = () => so(t), t;
}, { round: vh } = Math;
V.prototype.rgb = function(e = !0) {
  return e === !1 ? this._rgb.slice(0, 3) : this._rgb.slice(0, 3).map(vh);
};
V.prototype.rgba = function(e = !0) {
  return this._rgb.slice(0, 4).map((t, n) => n < 3 ? e === !1 ? t : vh(t) : t);
};
const F1 = (...e) => new V(...e, "rgb");
Object.assign(q, { rgb: F1 });
J.format.rgb = (...e) => {
  const t = Q(e, "rgba");
  return t[3] === void 0 && (t[3] = 1), t;
};
J.autodetect.push({
  p: 3,
  test: (...e) => {
    if (e = Q(e, "rgba"), nt(e) === "array" && (e.length === 3 || e.length === 4 && nt(e[3]) == "number" && e[3] >= 0 && e[3] <= 1))
      return "rgb";
  }
});
const ge = (e, t, n) => {
  if (!ge[n])
    throw new Error("unknown blend mode " + n);
  return ge[n](e, t);
}, cn = (e) => (t, n) => {
  const s = q(n).rgb(), i = q(t).rgb();
  return q.rgb(e(s, i));
}, fn = (e) => (t, n) => {
  const s = [];
  return s[0] = e(t[0], n[0]), s[1] = e(t[1], n[1]), s[2] = e(t[2], n[2]), s;
}, $1 = (e) => e, B1 = (e, t) => e * t / 255, j1 = (e, t) => e > t ? t : e, z1 = (e, t) => e > t ? e : t, H1 = (e, t) => 255 * (1 - (1 - e / 255) * (1 - t / 255)), W1 = (e, t) => t < 128 ? 2 * e * t / 255 : 255 * (1 - 2 * (1 - e / 255) * (1 - t / 255)), U1 = (e, t) => 255 * (1 - (1 - t / 255) / (e / 255)), Y1 = (e, t) => e === 255 ? 255 : (e = 255 * (t / 255) / (1 - e / 255), e > 255 ? 255 : e);
ge.normal = cn(fn($1));
ge.multiply = cn(fn(B1));
ge.screen = cn(fn(H1));
ge.overlay = cn(fn(W1));
ge.darken = cn(fn(j1));
ge.lighten = cn(fn(z1));
ge.dodge = cn(fn(Y1));
ge.burn = cn(fn(U1));
const { pow: K1, sin: q1, cos: X1 } = Math;
function G1(e = 300, t = -1.5, n = 1, s = 1, i = [0, 1]) {
  let o = 0, r;
  nt(i) === "array" ? r = i[1] - i[0] : (r = 0, i = [i, i]);
  const a = function(l) {
    const c = He * ((e + 120) / 360 + t * l), f = K1(i[0] + r * l, s), h = (o !== 0 ? n[0] + l * o : n) * f * (1 - f) / 2, d = X1(c), p = q1(c), g = f + h * (-0.14861 * d + 1.78277 * p), b = f + h * (-0.29227 * d - 0.90649 * p), y = f + h * (1.97294 * d);
    return q(Ea([g * 255, b * 255, y * 255, 1]));
  };
  return a.start = function(l) {
    return l == null ? e : (e = l, a);
  }, a.rotations = function(l) {
    return l == null ? t : (t = l, a);
  }, a.gamma = function(l) {
    return l == null ? s : (s = l, a);
  }, a.hue = function(l) {
    return l == null ? n : (n = l, nt(n) === "array" ? (o = n[1] - n[0], o === 0 && (n = n[1])) : o = 0, a);
  }, a.lightness = function(l) {
    return l == null ? i : (nt(l) === "array" ? (i = l, r = l[1] - l[0]) : (i = [l, l], r = 0), a);
  }, a.scale = () => q.scale(a), a.hue(n), a;
}
const Z1 = "0123456789abcdef", { floor: J1, random: Q1 } = Math, tx = () => {
  let e = "#";
  for (let t = 0; t < 6; t++)
    e += Z1.charAt(J1(Q1() * 16));
  return new V(e, "hex");
}, { log: zc, pow: ex, floor: nx, abs: sx } = Math;
function wh(e, t = null) {
  const n = {
    min: Number.MAX_VALUE,
    max: Number.MAX_VALUE * -1,
    sum: 0,
    values: [],
    count: 0
  };
  return nt(e) === "object" && (e = Object.values(e)), e.forEach((s) => {
    t && nt(s) === "object" && (s = s[t]), s != null && !isNaN(s) && (n.values.push(s), n.sum += s, s < n.min && (n.min = s), s > n.max && (n.max = s), n.count += 1);
  }), n.domain = [n.min, n.max], n.limits = (s, i) => Eh(n, s, i), n;
}
function Eh(e, t = "equal", n = 7) {
  nt(e) == "array" && (e = wh(e));
  const { min: s, max: i } = e, o = e.values.sort((a, l) => a - l);
  if (n === 1)
    return [s, i];
  const r = [];
  if (t.substr(0, 1) === "c" && (r.push(s), r.push(i)), t.substr(0, 1) === "e") {
    r.push(s);
    for (let a = 1; a < n; a++)
      r.push(s + a / n * (i - s));
    r.push(i);
  } else if (t.substr(0, 1) === "l") {
    if (s <= 0)
      throw new Error(
        "Logarithmic scales are only possible for values > 0"
      );
    const a = Math.LOG10E * zc(s), l = Math.LOG10E * zc(i);
    r.push(s);
    for (let c = 1; c < n; c++)
      r.push(ex(10, a + c / n * (l - a)));
    r.push(i);
  } else if (t.substr(0, 1) === "q") {
    r.push(s);
    for (let a = 1; a < n; a++) {
      const l = (o.length - 1) * a / n, c = nx(l);
      if (c === l)
        r.push(o[c]);
      else {
        const f = l - c;
        r.push(o[c] * (1 - f) + o[c + 1] * f);
      }
    }
    r.push(i);
  } else if (t.substr(0, 1) === "k") {
    let a;
    const l = o.length, c = new Array(l), f = new Array(n);
    let u = !0, h = 0, d = null;
    d = [], d.push(s);
    for (let b = 1; b < n; b++)
      d.push(s + b / n * (i - s));
    for (d.push(i); u; ) {
      for (let y = 0; y < n; y++)
        f[y] = 0;
      for (let y = 0; y < l; y++) {
        const O = o[y];
        let M = Number.MAX_VALUE, P;
        for (let w = 0; w < n; w++) {
          const k = sx(d[w] - O);
          k < M && (M = k, P = w), f[P]++, c[y] = P;
        }
      }
      const b = new Array(n);
      for (let y = 0; y < n; y++)
        b[y] = null;
      for (let y = 0; y < l; y++)
        a = c[y], b[a] === null ? b[a] = o[y] : b[a] += o[y];
      for (let y = 0; y < n; y++)
        b[y] *= 1 / f[y];
      u = !1;
      for (let y = 0; y < n; y++)
        if (b[y] !== d[y]) {
          u = !0;
          break;
        }
      d = b, h++, h > 200 && (u = !1);
    }
    const p = {};
    for (let b = 0; b < n; b++)
      p[b] = [];
    for (let b = 0; b < l; b++)
      a = c[b], p[a].push(o[b]);
    let g = [];
    for (let b = 0; b < n; b++)
      g.push(p[b][0]), g.push(p[b][p[b].length - 1]);
    g = g.sort((b, y) => b - y), r.push(g[0]);
    for (let b = 1; b < g.length; b += 2) {
      const y = g[b];
      !isNaN(y) && r.indexOf(y) === -1 && r.push(y);
    }
  }
  return r;
}
const ix = (e, t) => {
  e = new V(e), t = new V(t);
  const n = e.luminance(), s = t.luminance();
  return n > s ? (n + 0.05) / (s + 0.05) : (s + 0.05) / (n + 0.05);
};
/**
 * @license
 *
 * The APCA contrast prediction algorithm is based of the formulas published
 * in the APCA-1.0.98G specification by Myndex. The specification is available at:
 * https://raw.githubusercontent.com/Myndex/apca-w3/master/images/APCAw3_0.1.17_APCA0.0.98G.svg
 *
 * Note that the APCA implementation is still beta, so please update to
 * future versions of chroma.js when they become available.
 *
 * You can read more about the APCA Readability Criterion at
 * https://readtech.org/ARC/
 */
const Hc = 0.027, ox = 5e-4, rx = 0.1, Wc = 1.14, yi = 0.022, Uc = 1.414, ax = (e, t) => {
  e = new V(e), t = new V(t), e.alpha() < 1 && (e = Zn(t, e, e.alpha(), "rgb"));
  const n = Yc(...e.rgb()), s = Yc(...t.rgb()), i = n >= yi ? n : n + Math.pow(yi - n, Uc), o = s >= yi ? s : s + Math.pow(yi - s, Uc), r = Math.pow(o, 0.56) - Math.pow(i, 0.57), a = Math.pow(o, 0.65) - Math.pow(i, 0.62), l = Math.abs(o - i) < ox ? 0 : i < o ? r * Wc : a * Wc;
  return (Math.abs(l) < rx ? 0 : l > 0 ? l - Hc : l + Hc) * 100;
};
function Yc(e, t, n) {
  return 0.2126729 * Math.pow(e / 255, 2.4) + 0.7151522 * Math.pow(t / 255, 2.4) + 0.072175 * Math.pow(n / 255, 2.4);
}
const { sqrt: Fe, pow: xt, min: lx, max: cx, atan2: Kc, abs: qc, cos: xi, sin: Xc, exp: fx, PI: Gc } = Math;
function ux(e, t, n = 1, s = 1, i = 1) {
  var o = function(Nt) {
    return 360 * Nt / (2 * Gc);
  }, r = function(Nt) {
    return 2 * Gc * Nt / 360;
  };
  e = new V(e), t = new V(t);
  const [a, l, c] = Array.from(e.lab()), [f, u, h] = Array.from(t.lab()), d = (a + f) / 2, p = Fe(xt(l, 2) + xt(c, 2)), g = Fe(xt(u, 2) + xt(h, 2)), b = (p + g) / 2, y = 0.5 * (1 - Fe(xt(b, 7) / (xt(b, 7) + xt(25, 7)))), O = l * (1 + y), M = u * (1 + y), P = Fe(xt(O, 2) + xt(c, 2)), w = Fe(xt(M, 2) + xt(h, 2)), k = (P + w) / 2, v = o(Kc(c, O)), S = o(Kc(h, M)), D = v >= 0 ? v : v + 360, F = S >= 0 ? S : S + 360, z = qc(D - F) > 180 ? (D + F + 360) / 2 : (D + F) / 2, j = 1 - 0.17 * xi(r(z - 30)) + 0.24 * xi(r(2 * z)) + 0.32 * xi(r(3 * z + 6)) - 0.2 * xi(r(4 * z - 63));
  let tt = F - D;
  tt = qc(tt) <= 180 ? tt : F <= D ? tt + 360 : tt - 360, tt = 2 * Fe(P * w) * Xc(r(tt) / 2);
  const Et = f - a, it = w - P, st = 1 + 0.015 * xt(d - 50, 2) / Fe(20 + xt(d - 50, 2)), W = 1 + 0.045 * k, G = 1 + 0.015 * k * j, Ct = 30 * fx(-xt((z - 275) / 25, 2)), ee = -(2 * Fe(xt(k, 7) / (xt(k, 7) + xt(25, 7)))) * Xc(2 * r(Ct)), It = Fe(
    xt(Et / (n * st), 2) + xt(it / (s * W), 2) + xt(tt / (i * G), 2) + ee * (it / (s * W)) * (tt / (i * G))
  );
  return cx(0, lx(100, It));
}
function hx(e, t, n = "lab") {
  e = new V(e), t = new V(t);
  const s = e.get(n), i = t.get(n);
  let o = 0;
  for (let r in s) {
    const a = (s[r] || 0) - (i[r] || 0);
    o += a * a;
  }
  return Math.sqrt(o);
}
const dx = (...e) => {
  try {
    return new V(...e), !0;
  } catch {
    return !1;
  }
}, px = {
  cool() {
    return so([q.hsl(180, 1, 0.9), q.hsl(250, 0.7, 0.4)]);
  },
  hot() {
    return so(["#000", "#f00", "#ff0", "#fff"]).mode(
      "rgb"
    );
  }
}, Br = {
  // sequential
  OrRd: ["#fff7ec", "#fee8c8", "#fdd49e", "#fdbb84", "#fc8d59", "#ef6548", "#d7301f", "#b30000", "#7f0000"],
  PuBu: ["#fff7fb", "#ece7f2", "#d0d1e6", "#a6bddb", "#74a9cf", "#3690c0", "#0570b0", "#045a8d", "#023858"],
  BuPu: ["#f7fcfd", "#e0ecf4", "#bfd3e6", "#9ebcda", "#8c96c6", "#8c6bb1", "#88419d", "#810f7c", "#4d004b"],
  Oranges: ["#fff5eb", "#fee6ce", "#fdd0a2", "#fdae6b", "#fd8d3c", "#f16913", "#d94801", "#a63603", "#7f2704"],
  BuGn: ["#f7fcfd", "#e5f5f9", "#ccece6", "#99d8c9", "#66c2a4", "#41ae76", "#238b45", "#006d2c", "#00441b"],
  YlOrBr: ["#ffffe5", "#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02", "#993404", "#662506"],
  YlGn: ["#ffffe5", "#f7fcb9", "#d9f0a3", "#addd8e", "#78c679", "#41ab5d", "#238443", "#006837", "#004529"],
  Reds: ["#fff5f0", "#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d", "#a50f15", "#67000d"],
  RdPu: ["#fff7f3", "#fde0dd", "#fcc5c0", "#fa9fb5", "#f768a1", "#dd3497", "#ae017e", "#7a0177", "#49006a"],
  Greens: ["#f7fcf5", "#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476", "#41ab5d", "#238b45", "#006d2c", "#00441b"],
  YlGnBu: ["#ffffd9", "#edf8b1", "#c7e9b4", "#7fcdbb", "#41b6c4", "#1d91c0", "#225ea8", "#253494", "#081d58"],
  Purples: ["#fcfbfd", "#efedf5", "#dadaeb", "#bcbddc", "#9e9ac8", "#807dba", "#6a51a3", "#54278f", "#3f007d"],
  GnBu: ["#f7fcf0", "#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe", "#0868ac", "#084081"],
  Greys: ["#ffffff", "#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696", "#737373", "#525252", "#252525", "#000000"],
  YlOrRd: ["#ffffcc", "#ffeda0", "#fed976", "#feb24c", "#fd8d3c", "#fc4e2a", "#e31a1c", "#bd0026", "#800026"],
  PuRd: ["#f7f4f9", "#e7e1ef", "#d4b9da", "#c994c7", "#df65b0", "#e7298a", "#ce1256", "#980043", "#67001f"],
  Blues: ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6", "#4292c6", "#2171b5", "#08519c", "#08306b"],
  PuBuGn: ["#fff7fb", "#ece2f0", "#d0d1e6", "#a6bddb", "#67a9cf", "#3690c0", "#02818a", "#016c59", "#014636"],
  Viridis: ["#440154", "#482777", "#3f4a8a", "#31678e", "#26838f", "#1f9d8a", "#6cce5a", "#b6de2b", "#fee825"],
  // diverging
  Spectral: ["#9e0142", "#d53e4f", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#e6f598", "#abdda4", "#66c2a5", "#3288bd", "#5e4fa2"],
  RdYlGn: ["#a50026", "#d73027", "#f46d43", "#fdae61", "#fee08b", "#ffffbf", "#d9ef8b", "#a6d96a", "#66bd63", "#1a9850", "#006837"],
  RdBu: ["#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#f7f7f7", "#d1e5f0", "#92c5de", "#4393c3", "#2166ac", "#053061"],
  PiYG: ["#8e0152", "#c51b7d", "#de77ae", "#f1b6da", "#fde0ef", "#f7f7f7", "#e6f5d0", "#b8e186", "#7fbc41", "#4d9221", "#276419"],
  PRGn: ["#40004b", "#762a83", "#9970ab", "#c2a5cf", "#e7d4e8", "#f7f7f7", "#d9f0d3", "#a6dba0", "#5aae61", "#1b7837", "#00441b"],
  RdYlBu: ["#a50026", "#d73027", "#f46d43", "#fdae61", "#fee090", "#ffffbf", "#e0f3f8", "#abd9e9", "#74add1", "#4575b4", "#313695"],
  BrBG: ["#543005", "#8c510a", "#bf812d", "#dfc27d", "#f6e8c3", "#f5f5f5", "#c7eae5", "#80cdc1", "#35978f", "#01665e", "#003c30"],
  RdGy: ["#67001f", "#b2182b", "#d6604d", "#f4a582", "#fddbc7", "#ffffff", "#e0e0e0", "#bababa", "#878787", "#4d4d4d", "#1a1a1a"],
  PuOr: ["#7f3b08", "#b35806", "#e08214", "#fdb863", "#fee0b6", "#f7f7f7", "#d8daeb", "#b2abd2", "#8073ac", "#542788", "#2d004b"],
  // qualitative
  Set2: ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"],
  Accent: ["#7fc97f", "#beaed4", "#fdc086", "#ffff99", "#386cb0", "#f0027f", "#bf5b17", "#666666"],
  Set1: ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33", "#a65628", "#f781bf", "#999999"],
  Set3: ["#8dd3c7", "#ffffb3", "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#d9d9d9", "#bc80bd", "#ccebc5", "#ffed6f"],
  Dark2: ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d", "#666666"],
  Paired: ["#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#ffff99", "#b15928"],
  Pastel2: ["#b3e2cd", "#fdcdac", "#cbd5e8", "#f4cae4", "#e6f5c9", "#fff2ae", "#f1e2cc", "#cccccc"],
  Pastel1: ["#fbb4ae", "#b3cde3", "#ccebc5", "#decbe4", "#fed9a6", "#ffffcc", "#e5d8bd", "#fddaec", "#f2f2f2"]
}, Oh = Object.keys(Br), Zc = new Map(Oh.map((e) => [e.toLowerCase(), e])), gx = typeof Proxy == "function" ? new Proxy(Br, {
  get(e, t) {
    const n = t.toLowerCase();
    if (Zc.has(n))
      return e[Zc.get(n)];
  },
  getOwnPropertyNames() {
    return Object.getOwnPropertyNames(Oh);
  }
}) : Br, mx = (...e) => {
  e = Q(e, "cmyk");
  const [t, n, s, i] = e, o = e.length > 4 ? e[4] : 1;
  return i === 1 ? [0, 0, 0, o] : [
    t >= 1 ? 0 : 255 * (1 - t) * (1 - i),
    // r
    n >= 1 ? 0 : 255 * (1 - n) * (1 - i),
    // g
    s >= 1 ? 0 : 255 * (1 - s) * (1 - i),
    // b
    o
  ];
}, { max: Jc } = Math, bx = (...e) => {
  let [t, n, s] = Q(e, "rgb");
  t = t / 255, n = n / 255, s = s / 255;
  const i = 1 - Jc(t, Jc(n, s)), o = i < 1 ? 1 / (1 - i) : 0, r = (1 - t - i) * o, a = (1 - n - i) * o, l = (1 - s - i) * o;
  return [r, a, l, i];
};
V.prototype.cmyk = function() {
  return bx(this._rgb);
};
const _x = (...e) => new V(...e, "cmyk");
Object.assign(q, { cmyk: _x });
J.format.cmyk = mx;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "cmyk"), nt(e) === "array" && e.length === 4)
      return "cmyk";
  }
});
const yx = (...e) => {
  const t = Q(e, "hsla");
  let n = es(e) || "lsa";
  return t[0] = ie(t[0] || 0) + "deg", t[1] = ie(t[1] * 100) + "%", t[2] = ie(t[2] * 100) + "%", n === "hsla" || t.length > 3 && t[3] < 1 ? (t[3] = "/ " + (t.length > 3 ? t[3] : 1), n = "hsla") : t.length = 3, `${n.substr(0, 3)}(${t.join(" ")})`;
}, xx = (...e) => {
  const t = Q(e, "lab");
  let n = es(e) || "lab";
  return t[0] = ie(t[0]) + "%", t[1] = ie(t[1]), t[2] = ie(t[2]), n === "laba" || t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `lab(${t.join(" ")})`;
}, vx = (...e) => {
  const t = Q(e, "lch");
  let n = es(e) || "lab";
  return t[0] = ie(t[0]) + "%", t[1] = ie(t[1]), t[2] = isNaN(t[2]) ? "none" : ie(t[2]) + "deg", n === "lcha" || t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `lch(${t.join(" ")})`;
}, wx = (...e) => {
  const t = Q(e, "lab");
  return t[0] = ie(t[0] * 100) + "%", t[1] = Fr(t[1]), t[2] = Fr(t[2]), t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `oklab(${t.join(" ")})`;
}, Sh = (...e) => {
  const [t, n, s, ...i] = Q(e, "rgb"), [o, r, a] = Da(t, n, s), [l, c, f] = _h(o, r, a);
  return [l, c, f, ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
}, Ex = (...e) => {
  const t = Q(e, "lch");
  return t[0] = ie(t[0] * 100) + "%", t[1] = Fr(t[1]), t[2] = isNaN(t[2]) ? "none" : ie(t[2]) + "deg", t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `oklch(${t.join(" ")})`;
}, { round: or } = Math, Ox = (...e) => {
  const t = Q(e, "rgba");
  let n = es(e) || "rgb";
  if (n.substr(0, 3) === "hsl")
    return yx(xh(t), n);
  if (n.substr(0, 3) === "lab") {
    const s = Ws();
    We("d50");
    const i = xx(Sa(t), n);
    return We(s), i;
  }
  if (n.substr(0, 3) === "lch") {
    const s = Ws();
    We("d50");
    const i = vx(ka(t), n);
    return We(s), i;
  }
  return n.substr(0, 5) === "oklab" ? wx(Da(t)) : n.substr(0, 5) === "oklch" ? Ex(Sh(t)) : (t[0] = or(t[0]), t[1] = or(t[1]), t[2] = or(t[2]), (n === "rgba" || t.length > 3 && t[3] < 1) && (t[3] = "/ " + (t.length > 3 ? t[3] : 1), n = "rgba"), `${n.substr(0, 3)}(${t.slice(0, n === "rgb" ? 3 : 4).join(" ")})`);
}, Mh = (...e) => {
  e = Q(e, "lch");
  const [t, n, s, ...i] = e, [o, r, a] = bh(t, n, s), [l, c, f] = Na(o, r, a);
  return [l, c, f, ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
}, Ue = /((?:-?\d+)|(?:-?\d+(?:\.\d+)?)%|none)/.source, pe = /((?:-?(?:\d+(?:\.\d*)?|\.\d+)%?)|none)/.source, io = /((?:-?(?:\d+(?:\.\d*)?|\.\d+)%)|none)/.source, oe = /\s*/.source, ss = /\s+/.source, Ca = /\s*,\s*/.source, Eo = /((?:-?(?:\d+(?:\.\d*)?|\.\d+)(?:deg)?)|none)/.source, is = /\s*(?:\/\s*((?:[01]|[01]?\.\d+)|\d+(?:\.\d+)?%))?/.source, kh = new RegExp(
  "^rgba?\\(" + oe + [Ue, Ue, Ue].join(ss) + is + "\\)$"
), Nh = new RegExp(
  "^rgb\\(" + oe + [Ue, Ue, Ue].join(Ca) + oe + "\\)$"
), Dh = new RegExp(
  "^rgba\\(" + oe + [Ue, Ue, Ue, pe].join(Ca) + oe + "\\)$"
), Ch = new RegExp(
  "^hsla?\\(" + oe + [Eo, io, io].join(ss) + is + "\\)$"
), Ph = new RegExp(
  "^hsl?\\(" + oe + [Eo, io, io].join(Ca) + oe + "\\)$"
), Th = /^hsla\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*,\s*([01]|[01]?\.\d+)\)$/, Ah = new RegExp(
  "^lab\\(" + oe + [pe, pe, pe].join(ss) + is + "\\)$"
), Vh = new RegExp(
  "^lch\\(" + oe + [pe, pe, Eo].join(ss) + is + "\\)$"
), Rh = new RegExp(
  "^oklab\\(" + oe + [pe, pe, pe].join(ss) + is + "\\)$"
), Ih = new RegExp(
  "^oklch\\(" + oe + [pe, pe, Eo].join(ss) + is + "\\)$"
), { round: Lh } = Math, zn = (e) => e.map((t, n) => n <= 2 ? Pn(Lh(t), 0, 255) : t), vt = (e, t = 0, n = 100, s = !1) => (typeof e == "string" && e.endsWith("%") && (e = parseFloat(e.substring(0, e.length - 1)) / 100, s ? e = t + (e + 1) * 0.5 * (n - t) : e = t + e * (n - t)), +e), Ft = (e, t) => e === "none" ? t : e, Pa = (e) => {
  if (e = e.toLowerCase().trim(), e === "transparent")
    return [0, 0, 0, 0];
  let t;
  if (J.format.named)
    try {
      return J.format.named(e);
    } catch {
    }
  if ((t = e.match(kh)) || (t = e.match(Nh))) {
    let n = t.slice(1, 4);
    for (let i = 0; i < 3; i++)
      n[i] = +vt(Ft(n[i], 0), 0, 255);
    n = zn(n);
    const s = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return n[3] = s, n;
  }
  if (t = e.match(Dh)) {
    const n = t.slice(1, 5);
    for (let s = 0; s < 4; s++)
      n[s] = +vt(n[s], 0, 255);
    return n;
  }
  if ((t = e.match(Ch)) || (t = e.match(Ph))) {
    const n = t.slice(1, 4);
    n[0] = +Ft(n[0].replace("deg", ""), 0), n[1] = +vt(Ft(n[1], 0), 0, 100) * 0.01, n[2] = +vt(Ft(n[2], 0), 0, 100) * 0.01;
    const s = zn($r(n)), i = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return s[3] = i, s;
  }
  if (t = e.match(Th)) {
    const n = t.slice(1, 4);
    n[1] *= 0.01, n[2] *= 0.01;
    const s = $r(n);
    for (let i = 0; i < 3; i++)
      s[i] = Lh(s[i]);
    return s[3] = +t[4], s;
  }
  if (t = e.match(Ah)) {
    const n = t.slice(1, 4);
    n[0] = vt(Ft(n[0], 0), 0, 100), n[1] = vt(Ft(n[1], 0), -125, 125, !0), n[2] = vt(Ft(n[2], 0), -125, 125, !0);
    const s = Ws();
    We("d50");
    const i = zn(Oa(n));
    We(s);
    const o = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return i[3] = o, i;
  }
  if (t = e.match(Vh)) {
    const n = t.slice(1, 4);
    n[0] = vt(n[0], 0, 100), n[1] = vt(Ft(n[1], 0), 0, 150, !1), n[2] = +Ft(n[2].replace("deg", ""), 0);
    const s = Ws();
    We("d50");
    const i = zn(Ma(n));
    We(s);
    const o = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return i[3] = o, i;
  }
  if (t = e.match(Rh)) {
    const n = t.slice(1, 4);
    n[0] = vt(Ft(n[0], 0), 0, 1), n[1] = vt(Ft(n[1], 0), -0.4, 0.4, !0), n[2] = vt(Ft(n[2], 0), -0.4, 0.4, !0);
    const s = zn(Na(n)), i = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return s[3] = i, s;
  }
  if (t = e.match(Ih)) {
    const n = t.slice(1, 4);
    n[0] = vt(Ft(n[0], 0), 0, 1), n[1] = vt(Ft(n[1], 0), 0, 0.4, !1), n[2] = +Ft(n[2].replace("deg", ""), 0);
    const s = zn(Mh(n)), i = t[4] !== void 0 ? +vt(t[4], 0, 1) : 1;
    return s[3] = i, s;
  }
};
Pa.test = (e) => (
  // modern
  kh.test(e) || Ch.test(e) || Ah.test(e) || Vh.test(e) || Rh.test(e) || Ih.test(e) || // legacy
  Nh.test(e) || Dh.test(e) || Ph.test(e) || Th.test(e) || e === "transparent"
);
V.prototype.css = function(e) {
  return Ox(this._rgb, e);
};
const Sx = (...e) => new V(...e, "css");
q.css = Sx;
J.format.css = Pa;
J.autodetect.push({
  p: 5,
  test: (e, ...t) => {
    if (!t.length && nt(e) === "string" && Pa.test(e))
      return "css";
  }
});
J.format.gl = (...e) => {
  const t = Q(e, "rgba");
  return t[0] *= 255, t[1] *= 255, t[2] *= 255, t;
};
const Mx = (...e) => new V(...e, "gl");
q.gl = Mx;
V.prototype.gl = function() {
  const e = this._rgb;
  return [e[0] / 255, e[1] / 255, e[2] / 255, e[3]];
};
V.prototype.hex = function(e) {
  return ph(this._rgb, e);
};
const kx = (...e) => new V(...e, "hex");
q.hex = kx;
J.format.hex = dh;
J.autodetect.push({
  p: 4,
  test: (e, ...t) => {
    if (!t.length && nt(e) === "string" && [3, 4, 5, 6, 7, 8, 9].indexOf(e.length) >= 0)
      return "hex";
  }
});
const { log: vi } = Math, Fh = (e) => {
  const t = e / 100;
  let n, s, i;
  return t < 66 ? (n = 255, s = t < 6 ? 0 : -155.25485562709179 - 0.44596950469579133 * (s = t - 2) + 104.49216199393888 * vi(s), i = t < 20 ? 0 : -254.76935184120902 + 0.8274096064007395 * (i = t - 10) + 115.67994401066147 * vi(i)) : (n = 351.97690566805693 + 0.114206453784165 * (n = t - 55) - 40.25366309332127 * vi(n), s = 325.4494125711974 + 0.07943456536662342 * (s = t - 50) - 28.0852963507957 * vi(s), i = 255), [n, s, i, 1];
}, { round: Nx } = Math, Dx = (...e) => {
  const t = Q(e, "rgb"), n = t[0], s = t[2];
  let i = 1e3, o = 4e4;
  const r = 0.4;
  let a;
  for (; o - i > r; ) {
    a = (o + i) * 0.5;
    const l = Fh(a);
    l[2] / l[0] >= s / n ? o = a : i = a;
  }
  return Nx(a);
};
V.prototype.temp = V.prototype.kelvin = V.prototype.temperature = function() {
  return Dx(this._rgb);
};
const rr = (...e) => new V(...e, "temp");
Object.assign(q, { temp: rr, kelvin: rr, temperature: rr });
J.format.temp = J.format.kelvin = J.format.temperature = Fh;
V.prototype.oklch = function() {
  return Sh(this._rgb);
};
const Cx = (...e) => new V(...e, "oklch");
Object.assign(q, { oklch: Cx });
J.format.oklch = Mh;
J.autodetect.push({
  p: 2,
  test: (...e) => {
    if (e = Q(e, "oklch"), nt(e) === "array" && e.length === 3)
      return "oklch";
  }
});
Object.assign(q, {
  analyze: wh,
  average: P1,
  bezier: L1,
  blend: ge,
  brewer: gx,
  Color: V,
  colors: Gn,
  contrast: ix,
  contrastAPCA: ax,
  cubehelix: G1,
  deltaE: ux,
  distance: hx,
  input: J,
  interpolate: Zn,
  limits: Eh,
  mix: Zn,
  random: tx,
  scale: so,
  scales: px,
  valid: dx
});
const Px = { "dsfr-chart-colors-01": "#5C68E5", "dsfr-chart-colors-02": "#82B5F2", "dsfr-chart-colors-03": "#29598F", "dsfr-chart-colors-04": "#31A7AE", "dsfr-chart-colors-05": "#81EEF5", "dsfr-chart-colors-06": "#B478F1", "dsfr-chart-colors-07": "#CFB1F5", "dsfr-chart-colors-08": "#CECECE", "dsfr-chart-colors-09": "#DBDAFF", "dsfr-chart-colors-10": "#00005F", "dsfr-chart-colors-11": "#298641", "dsfr-chart-colors-12": "#79D289", "dsfr-chart-colors-13": "#EFB900", "dsfr-chart-colors-14": "#FFA373", "dsfr-chart-colors-15": "#E91719", "dsfr-chart-colors-default": "#5C68E5", "dsfr-chart-colors-neutral": "#B1B1B1" }, Tx = { "dsfr-chart-colors-01": "#5C68E5", "dsfr-chart-colors-02": "#699BD6", "dsfr-chart-colors-03": "#4878B1", "dsfr-chart-colors-04": "#00828A", "dsfr-chart-colors-05": "#51C1C8", "dsfr-chart-colors-06": "#BC8AF2", "dsfr-chart-colors-07": "#CFB1F5", "dsfr-chart-colors-08": "#A4A4A4", "dsfr-chart-colors-09": "#B8B9FF", "dsfr-chart-colors-10": "#3647CA", "dsfr-chart-colors-11": "#298641", "dsfr-chart-colors-12": "#449D57", "dsfr-chart-colors-13": "#AF8800", "dsfr-chart-colors-14": "#FFA373", "dsfr-chart-colors-15": "#E16834", "dsfr-chart-colors-default": "#5C68E5", "dsfr-chart-colors-neutral": "#808080" }, Qc = {
  light: Px,
  dark: Tx
};
function Ax({
  yparse: e = [],
  tmpColorParse: t = [],
  highlightIndex: n = [],
  selectedPalette: s = "",
  reverseOrder: i = !1
}) {
  const o = [], r = [], a = jh(s), l = i ? [...e].reverse() : e;
  for (let f = 0; f < l.length; f++) {
    const u = l[f];
    let h = [], d = [];
    if (t[f]) {
      const p = t[f], g = u && u.length ? u.length : 1;
      h = Array(g).fill(p), d = h.map((b) => q(b).darken(0.8).hex());
    } else if (s === "neutral" && n.length > 0 && Array.isArray(u)) {
      const p = u && u.length ? u.length : 1;
      for (let g = 0; g < p; g++) {
        const b = n.includes(g) ? $h() : Bh();
        h.push(b), d.push(q(b).darken(0.8).hex());
      }
    } else if (s.startsWith("divergent")) {
      const p = u && u.length ? u.length : 1;
      h = Array(p).fill(a[f % a.length]), d = h.map((g) => q(g).darken(0.8).hex());
    } else if (s === "categorical" || !s) {
      const p = Fx(f, a), g = u && u.length ? u.length : 1;
      h = Array(g).fill(p), d = h.map((b) => q(b).darken(0.8).hex());
    } else {
      const p = e.flat(), g = Math.min(...p), b = Math.max(...p), y = q.scale(a).domain([b, g]);
      h = (u || [g]).map((M) => q(y(M)).hex()), d = h.map((M) => q(M).darken(0.8).hex());
    }
    o.push(h), r.push(d);
  }
  const c = i ? o.map((f) => f[0]).reverse() : o.map((f) => f[0]);
  return {
    colorParse: o,
    colorHover: r,
    legendColors: c
  };
}
function Rn() {
  const e = document.documentElement.getAttribute("data-fr-theme") || "light";
  return Qc[e] || Qc.light;
}
function jr() {
  const e = Rn();
  return [
    e["dsfr-chart-colors-01"],
    e["dsfr-chart-colors-02"],
    e["dsfr-chart-colors-03"],
    e["dsfr-chart-colors-04"],
    e["dsfr-chart-colors-05"],
    e["dsfr-chart-colors-06"],
    e["dsfr-chart-colors-07"],
    e["dsfr-chart-colors-08"]
  ];
}
function Vx() {
  const e = Rn();
  return q.scale([
    e["dsfr-chart-colors-09"],
    e["dsfr-chart-colors-10"]
  ]).colors(10);
}
function Rx() {
  const e = Rn();
  return q.scale([
    e["dsfr-chart-colors-10"],
    e["dsfr-chart-colors-09"]
  ]).colors(10);
}
function Ix() {
  const e = Rn();
  return q.scale([
    e["dsfr-chart-colors-11"],
    e["dsfr-chart-colors-13"],
    e["dsfr-chart-colors-15"]
  ]).colors(4);
}
function Lx() {
  const e = Rn();
  return q.scale([
    e["dsfr-chart-colors-15"],
    e["dsfr-chart-colors-13"],
    e["dsfr-chart-colors-11"]
  ]).colors(4);
}
function Fx(e, t = jr()) {
  return t[e % t.length];
}
function $h() {
  return Rn()["dsfr-chart-colors-default"];
}
function Bh() {
  return Rn()["dsfr-chart-colors-neutral"];
}
function jh(e) {
  switch (e) {
    case "default":
      return [$h()];
    case "neutral":
      return [Bh()];
    case "categorical":
      return jr();
    case "sequentialAscending":
      return Vx();
    case "sequentialDescending":
      return Rx();
    case "divergentAscending":
      return Ix();
    case "divergentDescending":
      return Lx();
    default:
      return jr();
  }
}
const $x = (e, t) => {
  const n = e.__vccOpts || e;
  for (const [s, i] of t)
    n[s] = i;
  return n;
};
Pt.register(Pi, Ri);
const Bx = {
  name: "BarChart",
  mixins: [ky],
  props: {
    databoxId: {
      type: String,
      default: null
    },
    databoxType: {
      type: String,
      default: null
    },
    databoxSource: {
      type: String,
      default: "default"
    },
    x: {
      type: String,
      required: !0
    },
    y: {
      type: String,
      required: !0
    },
    xMin: {
      type: [Number, String],
      default: ""
    },
    xMax: {
      type: [Number, String],
      default: ""
    },
    yMin: {
      type: [Number, String],
      default: ""
    },
    yMax: {
      type: [Number, String],
      default: ""
    },
    name: {
      type: String,
      default: ""
    },
    stacked: {
      type: [Boolean, String],
      default: !1
    },
    horizontal: {
      type: [Boolean, String],
      default: !1
    },
    barSize: {
      type: [Number, String],
      default: "flex"
    },
    maxBarSize: {
      type: [Number, String],
      default: 32
    },
    date: {
      type: String,
      default: ""
    },
    aspectRatio: {
      type: [Number, String],
      default: 2
    },
    selectedPalette: {
      type: String,
      default: ""
    },
    highlightIndex: {
      type: Array,
      default: () => [3, 4]
    },
    unitTooltip: {
      type: String,
      default: ""
    }
  },
  data() {
    return this.chart = void 0, {
      widgetId: "",
      chartId: "",
      datasets: [],
      labels: [],
      xparse: [],
      yparse: [],
      nameParse: [],
      tmpColorParse: [],
      colorParse: [],
      colorHover: [],
      legendColors: []
    };
  },
  created() {
    My(), this.chartId = "dsfr-chart-" + Math.floor(Math.random() * 1e3), this.widgetId = "dsfr-widget-" + Math.floor(Math.random() * 1e3);
  },
  mounted() {
    this.resetData(), this.createChart(), this.display = this.$refs[this.widgetId].offsetWidth > 486 ? "big" : "small", document.documentElement.addEventListener("dsfr.theme", (t) => {
      this.chartId !== "" && this.changeColors(t.detail.theme);
    });
  },
  methods: {
    resetData() {
      this.chart && this.chart.destroy(), this.datasets = [], this.labels = [], this.xparse = [], this.yparse = [], this.nameParse = [], this.tmpColorParse = [], this.colorParse = [], this.colorHover = [];
    },
    getData() {
      try {
        this.xparse = JSON.parse(this.x), this.yparse = JSON.parse(this.y);
      } catch (t) {
        console.error("Erreur lors du parsing des données x ou y:", t);
        return;
      }
      let e = [];
      if (this.name)
        try {
          e = JSON.parse(this.name);
        } catch (t) {
          console.error("Erreur lors du parsing de name:", t);
        }
      for (let t = 0; t < this.yparse.length; t++)
        e[t] ? this.nameParse.push(e[t]) : this.nameParse.push("Série " + (t + 1));
      this.labels = this.xparse[0], this.loadColors(), this.datasets = this.yparse.map((t, n) => ({
        label: this.nameParse[n],
        data: t,
        backgroundColor: this.colorParse[n],
        borderColor: this.colorParse[n],
        hoverBackgroundColor: this.colorHover[n],
        hoverBorderColor: this.colorHover[n],
        barThickness: this.barSize,
        ...this.maxBarSize ? { maxBarThickness: this.maxBarSize } : {}
      }));
    },
    choosePalette() {
      return jh(this.selectedPalette);
    },
    loadColors() {
      const { colorParse: e, colorHover: t, legendColors: n } = Ax({
        yparse: this.yparse,
        tmpColorParse: this.tmpColorParse,
        highlightIndex: this.highlightIndex,
        selectedPalette: this.selectedPalette,
        reverseOrder: this.selectedPalette === "divergentDescending"
      });
      this.colorParse = e, this.colorHover = t, this.legendColors = n;
    },
    createChart() {
      this.chart && this.chart.destroy(), this.getData();
      const e = this.$refs[this.chartId].getContext("2d");
      this.chart = new Pt(e, {
        type: "bar",
        data: {
          labels: this.labels,
          datasets: this.datasets
        },
        options: {
          indexAxis: this.horizontal ? "y" : "x",
          aspectRatio: this.aspectRatio,
          scales: {
            x: {
              offset: !this.horizontal,
              stacked: this.stacked,
              grid: {
                drawTicks: !1,
                drawOnChartArea: this.horizontal
              },
              ticks: {
                beginAtZero: !0,
                padding: this.horizontal ? 5 : 15
              },
              ...this.xMin ? { suggestedMin: this.xMin } : {},
              ...this.xMax ? { suggestedMax: this.xMax } : {}
            },
            y: {
              stacked: this.stacked,
              offset: this.horizontal,
              grid: {
                drawTicks: !1,
                drawOnChartArea: !this.horizontal
              },
              border: {
                dash: [3]
              },
              ticks: {
                beginAtZero: !0,
                padding: 5
              },
              ...this.yMin ? { suggestedMin: this.yMin } : {},
              ...this.yMax ? { suggestedMax: this.yMax } : {}
            }
          },
          plugins: {
            legend: {
              display: !1
            },
            tooltip: {
              enabled: !1,
              mode: "index",
              displayColors: !1,
              backgroundColor: "#6b6b6b",
              callbacks: {
                label: (t) => {
                  const n = this.datasets[t.datasetIndex].data[t.dataIndex];
                  return this.formatNumber(n);
                },
                title: (t) => t[0].label,
                labelTextColor: (t) => this.colorParse[t.datasetIndex][t.dataIndex]
              },
              external: (t) => {
                const s = (document.getElementById(this.databoxId + "-" + this.databoxType + "-" + this.databoxSource) || this.$el.nextElementSibling).querySelector(".tooltip"), i = t.tooltip;
                if (!s) return;
                if (!i || i.opacity === 0) {
                  s.style.opacity = 0;
                  return;
                }
                if (s.classList.remove("above", "below", "no-transform"), i.yAlign ? s.classList.add(i.yAlign) : s.classList.add("no-transform"), i.body) {
                  const u = i.title || [], h = s.querySelector(".tooltip_header.fr-text--sm.fr-mb-0");
                  h.innerHTML = u[0];
                  const d = s.querySelector(".tooltip_value");
                  d.innerHTML = "", i.dataPoints.forEach((p) => {
                    const g = p.datasetIndex, b = p.dataIndex, y = this.colorParse[g] ? this.colorParse[g][b] : "#000", M = `${this.formatNumber(this.datasets[g].data[b])}${this.unitTooltip ? " " + this.unitTooltip : ""}`;
                    d.innerHTML += `
                    <div class="tooltip_value-content">
                      <span class="tooltip_dot" style="background-color:${y};"></span>
                      <p class="tooltip_place fr-mb-0">${M}</p>
                    </div>
                  `;
                  });
                }
                const { offsetLeft: o, offsetTop: r } = this.chart.canvas, a = Number(this.chart.canvas.style.width.replace(/\D/g, "")), l = Number(this.chart.canvas.style.height.replace(/\D/g, ""));
                let c = o + i.caretX + 10, f = r + i.caretY - 20;
                c + s.clientWidth > o + a && (c = o + i.caretX - s.clientWidth - 10), f + s.clientHeight > r + 0.9 * l && (f = r + i.caretY - s.clientHeight + 20), c < o && (c = o + i.caretX - s.clientWidth / 2, f = r + i.caretY - s.clientHeight - 20), s.style.position = "absolute", s.style.padding = i.padding + "px " + i.padding + "px", s.style.pointerEvents = "none", s.style.left = c + "px", s.style.top = f + "px", s.style.opacity = 1;
              }
            }
          }
        }
      });
    },
    changeColors(e) {
      this.loadColors(), this.chart.data.datasets.forEach((t, n) => {
        t.borderColor = this.colorParse[n], t.backgroundColor = this.colorParse[n], t.hoverBorderColor = this.colorHover[n], t.hoverBackgroundColor = this.colorHover[n];
      }), this.chart.options.scales.x.ticks.color = e === "dark" ? "#cecece" : Pt.defaults.color, this.chart.options.scales.y.ticks.color = e === "dark" ? "#cecece" : Pt.defaults.color, this.chart.update("none");
    }
  }
}, jx = { class: "fr-col-12" }, zx = { class: "chart" }, Hx = { class: "chart_legend fr-mb-0 fr-mt-4v" }, Wx = { class: "fr-text--sm fr-text--bold fr-ml-1w fr-mb-0" }, Ux = {
  key: 0,
  class: "flex fr-mt-1w"
}, Yx = { class: "fr-text--xs" };
function Kx(e, t, n, s, i, o) {
  var r;
  return ys(), hu(sp, {
    disabled: !((r = e.$el) != null && r.ownerDocument.getElementById(n.databoxId)) || !n.databoxId && !n.databoxType && n.databoxSource === "default",
    to: "#" + n.databoxId + "-" + n.databoxType + "-" + n.databoxSource
  }, [
    Wt("div", {
      ref: i.widgetId,
      class: "widget_container fr-grid-row"
    }, [
      Wt("div", jx, [
        Wt("div", zx, [
          t[0] || (t[0] = Wt("div", { class: "tooltip" }, [
            Wt("div", { class: "tooltip_header fr-text--sm fr-mb-0" }),
            Wt("div", { class: "tooltip_body" }, [
              Wt("div", { class: "tooltip_value" })
            ])
          ], -1)),
          Wt("canvas", { ref: i.chartId }, null, 512),
          Wt("div", Hx, [
            (ys(!0), Vo(le, null, yp(i.nameParse, (a, l) => (ys(), Vo("div", {
              key: l,
              class: "flex fr-mt-3v fr-mb-1v"
            }, [
              Wt("span", {
                class: "legende_dot",
                style: co({ "background-color": i.legendColors[l] })
              }, null, 4),
              Wt("p", Wx, ar(e.capitalize(a)), 1)
            ]))), 128))
          ]),
          n.date ? (ys(), Vo("div", Ux, [
            Wt("p", Yx, " Mise à jour : " + ar(n.date), 1)
          ])) : fg("", !0)
        ])
      ])
    ], 512)
  ], 8, ["disabled", "to"]);
}
const qx = /* @__PURE__ */ $x(Bx, [["render", Kx]]), Xx = /* @__PURE__ */ Kg(qx);
customElements.define("bar-chart", Xx, { shadowRoot: !1 });
