//#region node_modules/@vue/shared/dist/shared.esm-bundler.js
// @__NO_SIDE_EFFECTS__
function e(e) {
	let t = /* @__PURE__ */ Object.create(null);
	for (let n of e.split(",")) t[n] = 1;
	return (e) => e in t;
}
var t = {}, n = [], r = () => {}, i = () => !1, a = (e) => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && (e.charCodeAt(2) > 122 || e.charCodeAt(2) < 97), o = (e) => e.startsWith("onUpdate:"), s = Object.assign, c = (e, t) => {
	let n = e.indexOf(t);
	n > -1 && e.splice(n, 1);
}, l = Object.prototype.hasOwnProperty, u = (e, t) => l.call(e, t), d = Array.isArray, f = (e) => x(e) === "[object Map]", p = (e) => x(e) === "[object Set]", m = (e) => x(e) === "[object Date]", h = (e) => typeof e == "function", g = (e) => typeof e == "string", _ = (e) => typeof e == "symbol", v = (e) => typeof e == "object" && !!e, y = (e) => (v(e) || h(e)) && h(e.then) && h(e.catch), b = Object.prototype.toString, x = (e) => b.call(e), S = (e) => x(e).slice(8, -1), C = (e) => x(e) === "[object Object]", w = (e) => g(e) && e !== "NaN" && e[0] !== "-" && "" + parseInt(e, 10) === e, T = /* @__PURE__ */ e(",key,ref,ref_for,ref_key,onVnodeBeforeMount,onVnodeMounted,onVnodeBeforeUpdate,onVnodeUpdated,onVnodeBeforeUnmount,onVnodeUnmounted"), E = (e) => {
	let t = /* @__PURE__ */ Object.create(null);
	return ((n) => t[n] || (t[n] = e(n)));
}, D = /-\w/g, O = E((e) => e.replace(D, (e) => e.slice(1).toUpperCase())), ee = /\B([A-Z])/g, k = E((e) => e.replace(ee, "-$1").toLowerCase()), te = E((e) => e.charAt(0).toUpperCase() + e.slice(1)), ne = E((e) => e ? `on${te(e)}` : ""), re = (e, t) => !Object.is(e, t), ie = (e, ...t) => {
	for (let n = 0; n < e.length; n++) e[n](...t);
}, A = (e, t, n, r = !1) => {
	Object.defineProperty(e, t, {
		configurable: !0,
		enumerable: !1,
		writable: r,
		value: n
	});
}, ae = (e) => {
	let t = parseFloat(e);
	return isNaN(t) ? e : t;
}, oe = (e) => {
	let t = g(e) ? Number(e) : NaN;
	return isNaN(t) ? e : t;
}, se, ce = () => se ||= typeof globalThis < "u" ? globalThis : typeof self < "u" ? self : typeof window < "u" ? window : typeof global < "u" ? global : {};
function le(e) {
	if (d(e)) {
		let t = {};
		for (let n = 0; n < e.length; n++) {
			let r = e[n], i = g(r) ? pe(r) : le(r);
			if (i) for (let e in i) t[e] = i[e];
		}
		return t;
	} else if (g(e) || v(e)) return e;
}
var ue = /;(?![^(]*\))/g, de = /:([^]+)/, fe = /\/\*[^]*?\*\//g;
function pe(e) {
	let t = {};
	return e.replace(fe, "").split(ue).forEach((e) => {
		if (e) {
			let n = e.split(de);
			n.length > 1 && (t[n[0].trim()] = n[1].trim());
		}
	}), t;
}
function me(e) {
	let t = "";
	if (g(e)) t = e;
	else if (d(e)) for (let n = 0; n < e.length; n++) {
		let r = me(e[n]);
		r && (t += r + " ");
	}
	else if (v(e)) for (let n in e) e[n] && (t += n + " ");
	return t.trim();
}
var he = "itemscope,allowfullscreen,formnovalidate,ismap,nomodule,novalidate,readonly", ge = /* @__PURE__ */ e(he);
he + "";
function _e(e) {
	return !!e || e === "";
}
function ve(e, t) {
	if (e.length !== t.length) return !1;
	let n = !0;
	for (let r = 0; n && r < e.length; r++) n = ye(e[r], t[r]);
	return n;
}
function ye(e, t) {
	if (e === t) return !0;
	let n = m(e), r = m(t);
	if (n || r) return n && r ? e.getTime() === t.getTime() : !1;
	if (n = _(e), r = _(t), n || r) return e === t;
	if (n = d(e), r = d(t), n || r) return n && r ? ve(e, t) : !1;
	if (n = v(e), r = v(t), n || r) {
		if (!n || !r || Object.keys(e).length !== Object.keys(t).length) return !1;
		for (let n in e) {
			let r = e.hasOwnProperty(n), i = t.hasOwnProperty(n);
			if (r && !i || !r && i || !ye(e[n], t[n])) return !1;
		}
	}
	return String(e) === String(t);
}
var be = (e) => !!(e && e.__v_isRef === !0), xe = (e) => g(e) ? e : e == null ? "" : d(e) || v(e) && (e.toString === b || !h(e.toString)) ? be(e) ? xe(e.value) : JSON.stringify(e, Se, 2) : String(e), Se = (e, t) => be(t) ? Se(e, t.value) : f(t) ? { [`Map(${t.size})`]: [...t.entries()].reduce((e, [t, n], r) => (e[Ce(t, r) + " =>"] = n, e), {}) } : p(t) ? { [`Set(${t.size})`]: [...t.values()].map((e) => Ce(e)) } : _(t) ? Ce(t) : v(t) && !d(t) && !C(t) ? String(t) : t, Ce = (e, t = "") => _(e) ? `Symbol(${e.description ?? t})` : e, j, we = class {
	constructor(e = !1) {
		this.detached = e, this._active = !0, this._on = 0, this.effects = [], this.cleanups = [], this._isPaused = !1, this._warnOnRun = !0, this.__v_skip = !0, !e && j && (j.active ? (this.parent = j, this.index = (j.scopes ||= []).push(this) - 1) : (this._active = !1, this._warnOnRun = !1));
	}
	get active() {
		return this._active;
	}
	pause() {
		if (this._active) {
			this._isPaused = !0;
			let e, t;
			if (this.scopes) for (e = 0, t = this.scopes.length; e < t; e++) this.scopes[e].pause();
			for (e = 0, t = this.effects.length; e < t; e++) this.effects[e].pause();
		}
	}
	resume() {
		if (this._active && this._isPaused) {
			this._isPaused = !1;
			let e, t;
			if (this.scopes) for (e = 0, t = this.scopes.length; e < t; e++) this.scopes[e].resume();
			for (e = 0, t = this.effects.length; e < t; e++) this.effects[e].resume();
		}
	}
	run(e) {
		if (this._active) {
			let t = j;
			try {
				return j = this, e();
			} finally {
				j = t;
			}
		}
	}
	on() {
		++this._on === 1 && (this.prevScope = j, j = this);
	}
	off() {
		if (this._on > 0 && --this._on === 0) {
			if (j === this) j = this.prevScope;
			else {
				let e = j;
				for (; e;) {
					if (e.prevScope === this) {
						e.prevScope = this.prevScope;
						break;
					}
					e = e.prevScope;
				}
			}
			this.prevScope = void 0;
		}
	}
	stop(e) {
		if (this._active) {
			this._active = !1;
			let t, n;
			for (t = 0, n = this.effects.length; t < n; t++) this.effects[t].stop();
			for (this.effects.length = 0, t = 0, n = this.cleanups.length; t < n; t++) this.cleanups[t]();
			if (this.cleanups.length = 0, this.scopes) {
				for (t = 0, n = this.scopes.length; t < n; t++) this.scopes[t].stop(!0);
				this.scopes.length = 0;
			}
			if (!this.detached && this.parent && !e) {
				let e = this.parent.scopes.pop();
				e && e !== this && (this.parent.scopes[this.index] = e, e.index = this.index);
			}
			this.parent = void 0;
		}
	}
};
function Te() {
	return j;
}
var M, Ee = /* @__PURE__ */ new WeakSet(), De = class {
	constructor(e) {
		this.fn = e, this.deps = void 0, this.depsTail = void 0, this.flags = 5, this.next = void 0, this.cleanup = void 0, this.scheduler = void 0, j && (j.active ? j.effects.push(this) : this.flags &= -2);
	}
	pause() {
		this.flags |= 64;
	}
	resume() {
		this.flags & 64 && (this.flags &= -65, Ee.has(this) && (Ee.delete(this), this.trigger()));
	}
	notify() {
		this.flags & 2 && !(this.flags & 32) || this.flags & 8 || je(this);
	}
	run() {
		if (!(this.flags & 1)) return this.fn();
		this.flags |= 2, We(this), Pe(this);
		let e = M, t = Be;
		M = this, Be = !0;
		try {
			return this.fn();
		} finally {
			Fe(this), M = e, Be = t, this.flags &= -3;
		}
	}
	stop() {
		if (this.flags & 1) {
			for (let e = this.deps; e; e = e.nextDep) Re(e);
			this.deps = this.depsTail = void 0, We(this), this.onStop && this.onStop(), this.flags &= -2;
		}
	}
	trigger() {
		this.flags & 64 ? Ee.add(this) : this.scheduler ? this.scheduler() : this.runIfDirty();
	}
	runIfDirty() {
		Ie(this) && this.run();
	}
	get dirty() {
		return Ie(this);
	}
}, Oe = 0, ke, Ae;
function je(e, t = !1) {
	if (e.flags |= 8, t) {
		e.next = Ae, Ae = e;
		return;
	}
	e.next = ke, ke = e;
}
function Me() {
	Oe++;
}
function Ne() {
	if (--Oe > 0) return;
	if (Ae) {
		let e = Ae;
		for (Ae = void 0; e;) {
			let t = e.next;
			e.next = void 0, e.flags &= -9, e = t;
		}
	}
	let e;
	for (; ke;) {
		let t = ke;
		for (ke = void 0; t;) {
			let n = t.next;
			if (t.next = void 0, t.flags &= -9, t.flags & 1) try {
				t.trigger();
			} catch (t) {
				e ||= t;
			}
			t = n;
		}
	}
	if (e) throw e;
}
function Pe(e) {
	for (let t = e.deps; t; t = t.nextDep) t.version = -1, t.prevActiveLink = t.dep.activeLink, t.dep.activeLink = t;
}
function Fe(e) {
	let t, n = e.depsTail, r = n;
	for (; r;) {
		let e = r.prevDep;
		r.version === -1 ? (r === n && (n = e), Re(r), ze(r)) : t = r, r.dep.activeLink = r.prevActiveLink, r.prevActiveLink = void 0, r = e;
	}
	e.deps = t, e.depsTail = n;
}
function Ie(e) {
	for (let t = e.deps; t; t = t.nextDep) if (t.dep.version !== t.version || t.dep.computed && (Le(t.dep.computed) || t.dep.version !== t.version)) return !0;
	return !!e._dirty;
}
function Le(e) {
	if (e.flags & 4 && !(e.flags & 16) || (e.flags &= -17, e.globalVersion === Ge) || (e.globalVersion = Ge, !e.isSSR && e.flags & 128 && (!e.deps && !e._dirty || !Ie(e)))) return;
	e.flags |= 2;
	let t = e.dep, n = M, r = Be;
	M = e, Be = !0;
	try {
		Pe(e);
		let n = e.fn(e._value);
		(t.version === 0 || re(n, e._value)) && (e.flags |= 128, e._value = n, t.version++);
	} catch (e) {
		throw t.version++, e;
	} finally {
		M = n, Be = r, Fe(e), e.flags &= -3;
	}
}
function Re(e, t = !1) {
	let { dep: n, prevSub: r, nextSub: i } = e;
	if (r && (r.nextSub = i, e.prevSub = void 0), i && (i.prevSub = r, e.nextSub = void 0), n.subs === e && (n.subs = r, !r && n.computed)) {
		n.computed.flags &= -5;
		for (let e = n.computed.deps; e; e = e.nextDep) Re(e, !0);
	}
	!t && !--n.sc && n.map && n.map.delete(n.key);
}
function ze(e) {
	let { prevDep: t, nextDep: n } = e;
	t && (t.nextDep = n, e.prevDep = void 0), n && (n.prevDep = t, e.nextDep = void 0);
}
var Be = !0, Ve = [];
function He() {
	Ve.push(Be), Be = !1;
}
function Ue() {
	let e = Ve.pop();
	Be = e === void 0 ? !0 : e;
}
function We(e) {
	let { cleanup: t } = e;
	if (e.cleanup = void 0, t) {
		let e = M;
		M = void 0;
		try {
			t();
		} finally {
			M = e;
		}
	}
}
var Ge = 0, Ke = class {
	constructor(e, t) {
		this.sub = e, this.dep = t, this.version = t.version, this.nextDep = this.prevDep = this.nextSub = this.prevSub = this.prevActiveLink = void 0;
	}
}, qe = class {
	constructor(e) {
		this.computed = e, this.version = 0, this.activeLink = void 0, this.subs = void 0, this.map = void 0, this.key = void 0, this.sc = 0, this.__v_skip = !0;
	}
	track(e) {
		if (!M || !Be || M === this.computed) return;
		let t = this.activeLink;
		if (t === void 0 || t.sub !== M) t = this.activeLink = new Ke(M, this), M.deps ? (t.prevDep = M.depsTail, M.depsTail.nextDep = t, M.depsTail = t) : M.deps = M.depsTail = t, Je(t);
		else if (t.version === -1 && (t.version = this.version, t.nextDep)) {
			let e = t.nextDep;
			e.prevDep = t.prevDep, t.prevDep && (t.prevDep.nextDep = e), t.prevDep = M.depsTail, t.nextDep = void 0, M.depsTail.nextDep = t, M.depsTail = t, M.deps === t && (M.deps = e);
		}
		return t;
	}
	trigger(e) {
		this.version++, Ge++, this.notify(e);
	}
	notify(e) {
		Me();
		try {
			for (let e = this.subs; e; e = e.prevSub) e.sub.notify() && e.sub.dep.notify();
		} finally {
			Ne();
		}
	}
};
function Je(e) {
	if (e.dep.sc++, e.sub.flags & 4) {
		let t = e.dep.computed;
		if (t && !e.dep.subs) {
			t.flags |= 20;
			for (let e = t.deps; e; e = e.nextDep) Je(e);
		}
		let n = e.dep.subs;
		n !== e && (e.prevSub = n, n && (n.nextSub = e)), e.dep.subs = e;
	}
}
var Ye = /* @__PURE__ */ new WeakMap(), Xe = /* @__PURE__ */ Symbol(""), Ze = /* @__PURE__ */ Symbol(""), Qe = /* @__PURE__ */ Symbol("");
function N(e, t, n) {
	if (Be && M) {
		let t = Ye.get(e);
		t || Ye.set(e, t = /* @__PURE__ */ new Map());
		let r = t.get(n);
		r || (t.set(n, r = new qe()), r.map = t, r.key = n), r.track();
	}
}
function $e(e, t, n, r, i, a) {
	let o = Ye.get(e);
	if (!o) {
		Ge++;
		return;
	}
	let s = (e) => {
		e && e.trigger();
	};
	if (Me(), t === "clear") o.forEach(s);
	else {
		let i = d(e), a = i && w(n);
		if (i && n === "length") {
			let e = Number(r);
			o.forEach((t, n) => {
				(n === "length" || n === Qe || !_(n) && n >= e) && s(t);
			});
		} else switch ((n !== void 0 || o.has(void 0)) && s(o.get(n)), a && s(o.get(Qe)), t) {
			case "add":
				i ? a && s(o.get("length")) : (s(o.get(Xe)), f(e) && s(o.get(Ze)));
				break;
			case "delete":
				i || (s(o.get(Xe)), f(e) && s(o.get(Ze)));
				break;
			case "set":
				f(e) && s(o.get(Xe));
				break;
		}
	}
	Ne();
}
function et(e) {
	let t = /* @__PURE__ */ P(e);
	return t === e ? t : (N(t, "iterate", Qe), /* @__PURE__ */ zt(e) ? t : t.map(Ht));
}
function tt(e) {
	return N(e = /* @__PURE__ */ P(e), "iterate", Qe), e;
}
function nt(e, t) {
	return /* @__PURE__ */ Rt(e) ? Ut(/* @__PURE__ */ Lt(e) ? Ht(t) : t) : Ht(t);
}
var rt = {
	__proto__: null,
	[Symbol.iterator]() {
		return it(this, Symbol.iterator, (e) => nt(this, e));
	},
	concat(...e) {
		return et(this).concat(...e.map((e) => d(e) ? et(e) : e));
	},
	entries() {
		return it(this, "entries", (e) => (e[1] = nt(this, e[1]), e));
	},
	every(e, t) {
		return ot(this, "every", e, t, void 0, arguments);
	},
	filter(e, t) {
		return ot(this, "filter", e, t, (e) => e.map((e) => nt(this, e)), arguments);
	},
	find(e, t) {
		return ot(this, "find", e, t, (e) => nt(this, e), arguments);
	},
	findIndex(e, t) {
		return ot(this, "findIndex", e, t, void 0, arguments);
	},
	findLast(e, t) {
		return ot(this, "findLast", e, t, (e) => nt(this, e), arguments);
	},
	findLastIndex(e, t) {
		return ot(this, "findLastIndex", e, t, void 0, arguments);
	},
	forEach(e, t) {
		return ot(this, "forEach", e, t, void 0, arguments);
	},
	includes(...e) {
		return ct(this, "includes", e);
	},
	indexOf(...e) {
		return ct(this, "indexOf", e);
	},
	join(e) {
		return et(this).join(e);
	},
	lastIndexOf(...e) {
		return ct(this, "lastIndexOf", e);
	},
	map(e, t) {
		return ot(this, "map", e, t, void 0, arguments);
	},
	pop() {
		return lt(this, "pop");
	},
	push(...e) {
		return lt(this, "push", e);
	},
	reduce(e, ...t) {
		return st(this, "reduce", e, t);
	},
	reduceRight(e, ...t) {
		return st(this, "reduceRight", e, t);
	},
	shift() {
		return lt(this, "shift");
	},
	some(e, t) {
		return ot(this, "some", e, t, void 0, arguments);
	},
	splice(...e) {
		return lt(this, "splice", e);
	},
	toReversed() {
		return et(this).toReversed();
	},
	toSorted(e) {
		return et(this).toSorted(e);
	},
	toSpliced(...e) {
		return et(this).toSpliced(...e);
	},
	unshift(...e) {
		return lt(this, "unshift", e);
	},
	values() {
		return it(this, "values", (e) => nt(this, e));
	}
};
function it(e, t, n) {
	let r = tt(e), i = r[t]();
	return r !== e && !/* @__PURE__ */ zt(e) && (i._next = i.next, i.next = () => {
		let e = i._next();
		return e.done || (e.value = n(e.value)), e;
	}), i;
}
var at = Array.prototype;
function ot(e, t, n, r, i, a) {
	let o = tt(e), s = o !== e && !/* @__PURE__ */ zt(e), c = o[t];
	if (c !== at[t]) {
		let t = c.apply(e, a);
		return s ? Ht(t) : t;
	}
	let l = n;
	o !== e && (s ? l = function(t, r) {
		return n.call(this, nt(e, t), r, e);
	} : n.length > 2 && (l = function(t, r) {
		return n.call(this, t, r, e);
	}));
	let u = c.call(o, l, r);
	return s && i ? i(u) : u;
}
function st(e, t, n, r) {
	let i = tt(e), a = i !== e && !/* @__PURE__ */ zt(e), o = n, s = !1;
	i !== e && (a ? (s = r.length === 0, o = function(t, r, i) {
		return s && (s = !1, t = nt(e, t)), n.call(this, t, nt(e, r), i, e);
	}) : n.length > 3 && (o = function(t, r, i) {
		return n.call(this, t, r, i, e);
	}));
	let c = i[t](o, ...r);
	return s ? nt(e, c) : c;
}
function ct(e, t, n) {
	let r = /* @__PURE__ */ P(e);
	N(r, "iterate", Qe);
	let i = r[t](...n);
	return (i === -1 || i === !1) && /* @__PURE__ */ Bt(n[0]) ? (n[0] = /* @__PURE__ */ P(n[0]), r[t](...n)) : i;
}
function lt(e, t, n = []) {
	He(), Me();
	let r = (/* @__PURE__ */ P(e))[t].apply(e, n);
	return Ne(), Ue(), r;
}
var ut = /* @__PURE__ */ e("__proto__,__v_isRef,__isVue"), dt = new Set(/* @__PURE__ */ Object.getOwnPropertyNames(Symbol).filter((e) => e !== "arguments" && e !== "caller").map((e) => Symbol[e]).filter(_));
function ft(e) {
	_(e) || (e = String(e));
	let t = /* @__PURE__ */ P(this);
	return N(t, "has", e), t.hasOwnProperty(e);
}
var pt = class {
	constructor(e = !1, t = !1) {
		this._isReadonly = e, this._isShallow = t;
	}
	get(e, t, n) {
		if (t === "__v_skip") return e.__v_skip;
		let r = this._isReadonly, i = this._isShallow;
		if (t === "__v_isReactive") return !r;
		if (t === "__v_isReadonly") return r;
		if (t === "__v_isShallow") return i;
		if (t === "__v_raw") return n === (r ? i ? jt : At : i ? kt : Ot).get(e) || Object.getPrototypeOf(e) === Object.getPrototypeOf(n) ? e : void 0;
		let a = d(e);
		if (!r) {
			let e;
			if (a && (e = rt[t])) return e;
			if (t === "hasOwnProperty") return ft;
		}
		let o = Reflect.get(e, t, /* @__PURE__ */ Wt(e) ? e : n);
		if ((_(t) ? dt.has(t) : ut(t)) || (r || N(e, "get", t), i)) return o;
		if (/* @__PURE__ */ Wt(o)) {
			let e = a && w(t) ? o : o.value;
			return r && v(e) ? /* @__PURE__ */ Ft(e) : e;
		}
		return v(o) ? r ? /* @__PURE__ */ Ft(o) : /* @__PURE__ */ Nt(o) : o;
	}
}, mt = class extends pt {
	constructor(e = !1) {
		super(!1, e);
	}
	set(e, t, n, r) {
		let i = e[t], a = d(e) && w(t);
		if (!this._isShallow) {
			let e = /* @__PURE__ */ Rt(i);
			if (!/* @__PURE__ */ zt(n) && !/* @__PURE__ */ Rt(n) && (i = /* @__PURE__ */ P(i), n = /* @__PURE__ */ P(n)), !a && /* @__PURE__ */ Wt(i) && !/* @__PURE__ */ Wt(n)) return e || (i.value = n), !0;
		}
		let o = a ? Number(t) < e.length : u(e, t), s = Reflect.set(e, t, n, /* @__PURE__ */ Wt(e) ? e : r);
		return e === /* @__PURE__ */ P(r) && (o ? re(n, i) && $e(e, "set", t, n, i) : $e(e, "add", t, n)), s;
	}
	deleteProperty(e, t) {
		let n = u(e, t), r = e[t], i = Reflect.deleteProperty(e, t);
		return i && n && $e(e, "delete", t, void 0, r), i;
	}
	has(e, t) {
		let n = Reflect.has(e, t);
		return (!_(t) || !dt.has(t)) && N(e, "has", t), n;
	}
	ownKeys(e) {
		return N(e, "iterate", d(e) ? "length" : Xe), Reflect.ownKeys(e);
	}
}, ht = class extends pt {
	constructor(e = !1) {
		super(!0, e);
	}
	set(e, t) {
		return !0;
	}
	deleteProperty(e, t) {
		return !0;
	}
}, gt = /* @__PURE__ */ new mt(), _t = /* @__PURE__ */ new ht(), vt = /* @__PURE__ */ new mt(!0), yt = (e) => e, bt = (e) => Reflect.getPrototypeOf(e);
function xt(e, t, n) {
	return function(...r) {
		let i = this.__v_raw, a = /* @__PURE__ */ P(i), o = f(a), c = e === "entries" || e === Symbol.iterator && o, l = e === "keys" && o, u = i[e](...r), d = n ? yt : t ? Ut : Ht;
		return !t && N(a, "iterate", l ? Ze : Xe), s(Object.create(u), { next() {
			let { value: e, done: t } = u.next();
			return t ? {
				value: e,
				done: t
			} : {
				value: c ? [d(e[0]), d(e[1])] : d(e),
				done: t
			};
		} });
	};
}
function St(e) {
	return function(...t) {
		return e === "delete" ? !1 : e === "clear" ? void 0 : this;
	};
}
function Ct(e, t) {
	let n = {
		get(n) {
			let r = this.__v_raw, i = /* @__PURE__ */ P(r), a = /* @__PURE__ */ P(n);
			e || (re(n, a) && N(i, "get", n), N(i, "get", a));
			let { has: o } = bt(i), s = t ? yt : e ? Ut : Ht;
			if (o.call(i, n)) return s(r.get(n));
			if (o.call(i, a)) return s(r.get(a));
			r !== i && r.get(n);
		},
		get size() {
			let t = this.__v_raw;
			return !e && N(/* @__PURE__ */ P(t), "iterate", Xe), t.size;
		},
		has(t) {
			let n = this.__v_raw, r = /* @__PURE__ */ P(n), i = /* @__PURE__ */ P(t);
			return e || (re(t, i) && N(r, "has", t), N(r, "has", i)), t === i ? n.has(t) : n.has(t) || n.has(i);
		},
		forEach(n, r) {
			let i = this, a = i.__v_raw, o = /* @__PURE__ */ P(a), s = t ? yt : e ? Ut : Ht;
			return !e && N(o, "iterate", Xe), a.forEach((e, t) => n.call(r, s(e), s(t), i));
		}
	};
	return s(n, e ? {
		add: St("add"),
		set: St("set"),
		delete: St("delete"),
		clear: St("clear")
	} : {
		add(e) {
			let n = /* @__PURE__ */ P(this), r = bt(n), i = /* @__PURE__ */ P(e), a = !t && !/* @__PURE__ */ zt(e) && !/* @__PURE__ */ Rt(e) ? i : e;
			return r.has.call(n, a) || re(e, a) && r.has.call(n, e) || re(i, a) && r.has.call(n, i) || (n.add(a), $e(n, "add", a, a)), this;
		},
		set(e, n) {
			!t && !/* @__PURE__ */ zt(n) && !/* @__PURE__ */ Rt(n) && (n = /* @__PURE__ */ P(n));
			let r = /* @__PURE__ */ P(this), { has: i, get: a } = bt(r), o = i.call(r, e);
			o ||= (e = /* @__PURE__ */ P(e), i.call(r, e));
			let s = a.call(r, e);
			return r.set(e, n), o ? re(n, s) && $e(r, "set", e, n, s) : $e(r, "add", e, n), this;
		},
		delete(e) {
			let t = /* @__PURE__ */ P(this), { has: n, get: r } = bt(t), i = n.call(t, e);
			i ||= (e = /* @__PURE__ */ P(e), n.call(t, e));
			let a = r ? r.call(t, e) : void 0, o = t.delete(e);
			return i && $e(t, "delete", e, void 0, a), o;
		},
		clear() {
			let e = /* @__PURE__ */ P(this), t = e.size !== 0, n = e.clear();
			return t && $e(e, "clear", void 0, void 0, void 0), n;
		}
	}), [
		"keys",
		"values",
		"entries",
		Symbol.iterator
	].forEach((r) => {
		n[r] = xt(r, e, t);
	}), n;
}
function wt(e, t) {
	let n = Ct(e, t);
	return (t, r, i) => r === "__v_isReactive" ? !e : r === "__v_isReadonly" ? e : r === "__v_raw" ? t : Reflect.get(u(n, r) && r in t ? n : t, r, i);
}
var Tt = { get: /* @__PURE__ */ wt(!1, !1) }, Et = { get: /* @__PURE__ */ wt(!1, !0) }, Dt = { get: /* @__PURE__ */ wt(!0, !1) }, Ot = /* @__PURE__ */ new WeakMap(), kt = /* @__PURE__ */ new WeakMap(), At = /* @__PURE__ */ new WeakMap(), jt = /* @__PURE__ */ new WeakMap();
function Mt(e) {
	switch (e) {
		case "Object":
		case "Array": return 1;
		case "Map":
		case "Set":
		case "WeakMap":
		case "WeakSet": return 2;
		default: return 0;
	}
}
// @__NO_SIDE_EFFECTS__
function Nt(e) {
	return /* @__PURE__ */ Rt(e) ? e : It(e, !1, gt, Tt, Ot);
}
// @__NO_SIDE_EFFECTS__
function Pt(e) {
	return It(e, !1, vt, Et, kt);
}
// @__NO_SIDE_EFFECTS__
function Ft(e) {
	return It(e, !0, _t, Dt, At);
}
function It(e, t, n, r, i) {
	if (!v(e) || e.__v_raw && !(t && e.__v_isReactive) || e.__v_skip || !Object.isExtensible(e)) return e;
	let a = i.get(e);
	if (a) return a;
	let o = Mt(S(e));
	if (o === 0) return e;
	let s = new Proxy(e, o === 2 ? r : n);
	return i.set(e, s), s;
}
// @__NO_SIDE_EFFECTS__
function Lt(e) {
	return /* @__PURE__ */ Rt(e) ? /* @__PURE__ */ Lt(e.__v_raw) : !!(e && e.__v_isReactive);
}
// @__NO_SIDE_EFFECTS__
function Rt(e) {
	return !!(e && e.__v_isReadonly);
}
// @__NO_SIDE_EFFECTS__
function zt(e) {
	return !!(e && e.__v_isShallow);
}
// @__NO_SIDE_EFFECTS__
function Bt(e) {
	return e ? !!e.__v_raw : !1;
}
// @__NO_SIDE_EFFECTS__
function P(e) {
	let t = e && e.__v_raw;
	return t ? /* @__PURE__ */ P(t) : e;
}
function Vt(e) {
	return !u(e, "__v_skip") && Object.isExtensible(e) && A(e, "__v_skip", !0), e;
}
var Ht = (e) => v(e) ? /* @__PURE__ */ Nt(e) : e, Ut = (e) => v(e) ? /* @__PURE__ */ Ft(e) : e;
// @__NO_SIDE_EFFECTS__
function Wt(e) {
	return e ? e.__v_isRef === !0 : !1;
}
function Gt(e) {
	return /* @__PURE__ */ Wt(e) ? e.value : e;
}
var Kt = {
	get: (e, t, n) => t === "__v_raw" ? e : Gt(Reflect.get(e, t, n)),
	set: (e, t, n, r) => {
		let i = e[t];
		return /* @__PURE__ */ Wt(i) && !/* @__PURE__ */ Wt(n) ? (i.value = n, !0) : Reflect.set(e, t, n, r);
	}
};
function qt(e) {
	return /* @__PURE__ */ Lt(e) ? e : new Proxy(e, Kt);
}
var Jt = class {
	constructor(e, t, n) {
		this.fn = e, this.setter = t, this._value = void 0, this.dep = new qe(this), this.__v_isRef = !0, this.deps = void 0, this.depsTail = void 0, this.flags = 16, this.globalVersion = Ge - 1, this.next = void 0, this.effect = this, this.__v_isReadonly = !t, this.isSSR = n;
	}
	notify() {
		if (this.flags |= 16, !(this.flags & 8) && M !== this) return je(this, !0), !0;
	}
	get value() {
		let e = this.dep.track();
		return Le(this), e && (e.version = this.dep.version), this._value;
	}
	set value(e) {
		this.setter && this.setter(e);
	}
};
// @__NO_SIDE_EFFECTS__
function Yt(e, t, n = !1) {
	let r, i;
	return h(e) ? r = e : (r = e.get, i = e.set), new Jt(r, i, n);
}
var Xt = {}, Zt = /* @__PURE__ */ new WeakMap(), Qt = void 0;
function $t(e, t = !1, n = Qt) {
	if (n) {
		let t = Zt.get(n);
		t || Zt.set(n, t = []), t.push(e);
	}
}
function en(e, n, i = t) {
	let { immediate: a, deep: o, once: s, scheduler: l, augmentJob: u, call: f } = i, p = (e) => o ? e : /* @__PURE__ */ zt(e) || o === !1 || o === 0 ? tn(e, 1) : tn(e), m, g, _, v, y = !1, b = !1;
	if (/* @__PURE__ */ Wt(e) ? (g = () => e.value, y = /* @__PURE__ */ zt(e)) : /* @__PURE__ */ Lt(e) ? (g = () => p(e), y = !0) : d(e) ? (b = !0, y = e.some((e) => /* @__PURE__ */ Lt(e) || /* @__PURE__ */ zt(e)), g = () => e.map((e) => {
		if (/* @__PURE__ */ Wt(e)) return e.value;
		if (/* @__PURE__ */ Lt(e)) return p(e);
		if (h(e)) return f ? f(e, 2) : e();
	})) : g = h(e) ? n ? f ? () => f(e, 2) : e : () => {
		if (_) {
			He();
			try {
				_();
			} finally {
				Ue();
			}
		}
		let t = Qt;
		Qt = m;
		try {
			return f ? f(e, 3, [v]) : e(v);
		} finally {
			Qt = t;
		}
	} : r, n && o) {
		let e = g, t = o === !0 ? Infinity : o;
		g = () => tn(e(), t);
	}
	let x = Te(), S = () => {
		m.stop(), x && x.active && c(x.effects, m);
	};
	if (s && n) {
		let e = n;
		n = (...t) => {
			e(...t), S();
		};
	}
	let C = b ? Array(e.length).fill(Xt) : Xt, w = (e) => {
		if (!(!(m.flags & 1) || !m.dirty && !e)) if (n) {
			let e = m.run();
			if (o || y || (b ? e.some((e, t) => re(e, C[t])) : re(e, C))) {
				_ && _();
				let t = Qt;
				Qt = m;
				try {
					let t = [
						e,
						C === Xt ? void 0 : b && C[0] === Xt ? [] : C,
						v
					];
					C = e, f ? f(n, 3, t) : n(...t);
				} finally {
					Qt = t;
				}
			}
		} else m.run();
	};
	return u && u(w), m = new De(g), m.scheduler = l ? () => l(w, !1) : w, v = (e) => $t(e, !1, m), _ = m.onStop = () => {
		let e = Zt.get(m);
		if (e) {
			if (f) f(e, 4);
			else for (let t of e) t();
			Zt.delete(m);
		}
	}, n ? a ? w(!0) : C = m.run() : l ? l(w.bind(null, !0), !0) : m.run(), S.pause = m.pause.bind(m), S.resume = m.resume.bind(m), S.stop = S, S;
}
function tn(e, t = Infinity, n) {
	if (t <= 0 || !v(e) || e.__v_skip || (n ||= /* @__PURE__ */ new Map(), (n.get(e) || 0) >= t)) return e;
	if (n.set(e, t), t--, /* @__PURE__ */ Wt(e)) tn(e.value, t, n);
	else if (d(e)) for (let r = 0; r < e.length; r++) tn(e[r], t, n);
	else if (p(e) || f(e)) e.forEach((e) => {
		tn(e, t, n);
	});
	else if (C(e)) {
		for (let r in e) tn(e[r], t, n);
		for (let r of Object.getOwnPropertySymbols(e)) Object.prototype.propertyIsEnumerable.call(e, r) && tn(e[r], t, n);
	}
	return e;
}
//#endregion
//#region node_modules/@vue/runtime-core/dist/runtime-core.esm-bundler.js
function nn(e, t, n, r) {
	try {
		return r ? e(...r) : e();
	} catch (e) {
		an(e, t, n);
	}
}
function rn(e, t, n, r) {
	if (h(e)) {
		let i = nn(e, t, n, r);
		return i && y(i) && i.catch((e) => {
			an(e, t, n);
		}), i;
	}
	if (d(e)) {
		let i = [];
		for (let a = 0; a < e.length; a++) i.push(rn(e[a], t, n, r));
		return i;
	}
}
function an(e, n, r, i = !0) {
	let a = n ? n.vnode : null, { errorHandler: o, throwUnhandledErrorInProduction: s } = n && n.appContext.config || t;
	if (n) {
		let t = n.parent, i = n.proxy, a = `https://vuejs.org/error-reference/#runtime-${r}`;
		for (; t;) {
			let n = t.ec;
			if (n) {
				for (let t = 0; t < n.length; t++) if (n[t](e, i, a) === !1) return;
			}
			t = t.parent;
		}
		if (o) {
			He(), nn(o, null, 10, [
				e,
				i,
				a
			]), Ue();
			return;
		}
	}
	on(e, r, a, i, s);
}
function on(e, t, n, r = !0, i = !1) {
	if (i) throw e;
	console.error(e);
}
var sn = [], cn = -1, ln = [], un = null, dn = 0, fn = /* @__PURE__ */ Promise.resolve(), pn = null;
function mn(e) {
	let t = pn || fn;
	return e ? t.then(this ? e.bind(this) : e) : t;
}
function hn(e) {
	let t = cn + 1, n = sn.length;
	for (; t < n;) {
		let r = t + n >>> 1, i = sn[r], a = xn(i);
		a < e || a === e && i.flags & 2 ? t = r + 1 : n = r;
	}
	return t;
}
function gn(e) {
	if (!(e.flags & 1)) {
		let t = xn(e), n = sn[sn.length - 1];
		!n || !(e.flags & 2) && t >= xn(n) ? sn.push(e) : sn.splice(hn(t), 0, e), e.flags |= 1, _n();
	}
}
function _n() {
	pn ||= fn.then(Sn);
}
function vn(e) {
	d(e) ? ln.push(...e) : un && e.id === -1 ? un.splice(dn + 1, 0, e) : e.flags & 1 || (ln.push(e), e.flags |= 1), _n();
}
function yn(e, t, n = cn + 1) {
	for (; n < sn.length; n++) {
		let t = sn[n];
		if (t && t.flags & 2) {
			if (e && t.id !== e.uid) continue;
			sn.splice(n, 1), n--, t.flags & 4 && (t.flags &= -2), t(), t.flags & 4 || (t.flags &= -2);
		}
	}
}
function bn(e) {
	if (ln.length) {
		let e = [...new Set(ln)].sort((e, t) => xn(e) - xn(t));
		if (ln.length = 0, un) {
			un.push(...e);
			return;
		}
		for (un = e, dn = 0; dn < un.length; dn++) {
			let e = un[dn];
			e.flags & 4 && (e.flags &= -2), e.flags & 8 || e(), e.flags &= -2;
		}
		un = null, dn = 0;
	}
}
var xn = (e) => e.id == null ? e.flags & 2 ? -1 : Infinity : e.id;
function Sn(e) {
	try {
		for (cn = 0; cn < sn.length; cn++) {
			let e = sn[cn];
			e && !(e.flags & 8) && (e.flags & 4 && (e.flags &= -2), nn(e, e.i, e.i ? 15 : 14), e.flags & 4 || (e.flags &= -2));
		}
	} finally {
		for (; cn < sn.length; cn++) {
			let e = sn[cn];
			e && (e.flags &= -2);
		}
		cn = -1, sn.length = 0, bn(e), pn = null, (sn.length || ln.length) && Sn(e);
	}
}
var Cn = null, wn = null;
function Tn(e) {
	let t = Cn;
	return Cn = e, wn = e && e.type.__scopeId || null, t;
}
function En(e, t = Cn, n) {
	if (!t || e._n) return e;
	let r = (...n) => {
		r._d && Gi(-1);
		let i = Tn(t), a;
		try {
			a = e(...n);
		} finally {
			Tn(i), r._d && Gi(1);
		}
		return a;
	};
	return r._n = !0, r._c = !0, r._d = !0, r;
}
function Dn(e, t, n, r) {
	let i = e.dirs, a = t && t.dirs;
	for (let o = 0; o < i.length; o++) {
		let s = i[o];
		a && (s.oldValue = a[o].value);
		let c = s.dir[r];
		c && (He(), rn(c, n, 8, [
			e.el,
			s,
			e,
			t
		]), Ue());
	}
}
function On(e, t) {
	if (I) {
		let n = I.provides, r = I.parent && I.parent.provides;
		r === n && (n = I.provides = Object.create(r)), n[e] = t;
	}
}
function kn(e, t, n = !1) {
	let r = ma();
	if (r || Kr) {
		let i = Kr ? Kr._context.provides : r ? r.parent == null || r.ce ? r.vnode.appContext && r.vnode.appContext.provides : r.parent.provides : void 0;
		if (i && e in i) return i[e];
		if (arguments.length > 1) return n && h(t) ? t.call(r && r.proxy) : t;
	}
}
var An = /* @__PURE__ */ Symbol.for("v-scx"), jn = () => kn(An);
function Mn(e, t, n) {
	return Nn(e, t, n);
}
function Nn(e, n, i = t) {
	let { immediate: a, deep: o, flush: c, once: l } = i, u = s({}, i), d = n && a || !n && c !== "post", f;
	if (ba) {
		if (c === "sync") {
			let e = jn();
			f = e.__watcherHandles ||= [];
		} else if (!d) {
			let e = () => {};
			return e.stop = r, e.resume = r, e.pause = r, e;
		}
	}
	let p = I;
	u.call = (e, t, n) => rn(e, p, t, n);
	let m = !1;
	c === "post" ? u.scheduler = (e) => {
		Ci(e, p && p.suspense);
	} : c !== "sync" && (m = !0, u.scheduler = (e, t) => {
		t ? e() : gn(e);
	}), u.augmentJob = (e) => {
		n && (e.flags |= 4), m && (e.flags |= 2, p && (e.id = p.uid, e.i = p));
	};
	let h = en(e, n, u);
	return ba && (f ? f.push(h) : d && h()), h;
}
function Pn(e, t, n) {
	let r = this.proxy, i = g(e) ? e.includes(".") ? Fn(r, e) : () => r[e] : e.bind(r, r), a;
	h(t) ? a = t : (a = t.handler, n = t);
	let o = _a(this), s = Nn(i, a.bind(r), n);
	return o(), s;
}
function Fn(e, t) {
	let n = t.split(".");
	return () => {
		let t = e;
		for (let e = 0; e < n.length && t; e++) t = t[n[e]];
		return t;
	};
}
var In = /* @__PURE__ */ new WeakMap(), Ln = /* @__PURE__ */ Symbol("_vte"), Rn = (e) => e.__isTeleport, zn = (e) => e && (e.disabled || e.disabled === ""), Bn = (e) => e && (e.defer || e.defer === ""), Vn = (e) => typeof SVGElement < "u" && e instanceof SVGElement, Hn = (e) => typeof MathMLElement == "function" && e instanceof MathMLElement, Un = (e, t) => {
	let n = e && e.to;
	return g(n) ? t ? t(n) : null : n;
}, Wn = {
	name: "Teleport",
	__isTeleport: !0,
	process(e, t, n, r, i, a, o, s, c, l) {
		let { mc: u, pc: d, pbc: f, o: { insert: p, querySelector: m, createText: h, createComment: g, parentNode: _ } } = l, v = zn(t.props), { dynamicChildren: y } = t, b = (e, t, n) => {
			e.shapeFlag & 16 && u(e.children, t, n, i, a, o, s, c);
		}, x = (e = t) => {
			let n = zn(e.props), r = e.target = Un(e.props, m), a = Yn(r, e, h, p);
			r && (o !== "svg" && Vn(r) ? o = "svg" : o !== "mathml" && Hn(r) && (o = "mathml"), i && i.isCE && (i.ce._teleportTargets || (i.ce._teleportTargets = /* @__PURE__ */ new Set())).add(r), n || (b(e, r, a), Jn(e, !1)));
		}, S = (e) => {
			let t = () => {
				In.get(e) === t && (In.delete(e), zn(e.props) && (b(e, _(e.el) || n, e.anchor), Jn(e, !0)), x(e));
			};
			In.set(e, t), Ci(t, a);
		};
		if (e == null) {
			let e = t.el = h(""), i = t.anchor = h("");
			if (p(e, n, r), p(i, n, r), Bn(t.props) || a && a.pendingBranch) {
				S(t);
				return;
			}
			v && (b(t, n, i), Jn(t, !0)), x();
		} else {
			t.el = e.el;
			let r = t.anchor = e.anchor, u = In.get(e);
			if (u) {
				u.flags |= 8, In.delete(e), S(t);
				return;
			}
			t.targetStart = e.targetStart;
			let p = t.target = e.target, h = t.targetAnchor = e.targetAnchor, g = zn(e.props), _ = g ? n : p, b = g ? r : h;
			if (o === "svg" || Vn(p) ? o = "svg" : (o === "mathml" || Hn(p)) && (o = "mathml"), y ? (f(e.dynamicChildren, y, _, i, a, o, s), ki(e, t, !0)) : c || d(e, t, _, b, i, a, o, s, !1), v) g ? t.props && e.props && t.props.to !== e.props.to && (t.props.to = e.props.to) : Gn(t, n, r, l, 1);
			else if ((t.props && t.props.to) !== (e.props && e.props.to)) {
				let e = t.target = Un(t.props, m);
				e && Gn(t, e, null, l, 0);
			} else g && Gn(t, p, h, l, 1);
			Jn(t, v);
		}
	},
	remove(e, t, n, { um: r, o: { remove: i } }, a) {
		let { shapeFlag: o, children: s, anchor: c, targetStart: l, targetAnchor: u, target: d, props: f } = e, p = a || !zn(f), m = In.get(e);
		if (m && (m.flags |= 8, In.delete(e)), d && (i(l), i(u)), a && i(c), !m && o & 16) for (let e = 0; e < s.length; e++) {
			let i = s[e];
			r(i, t, n, p, !!i.dynamicChildren);
		}
	},
	move: Gn,
	hydrate: Kn
};
function Gn(e, t, n, { o: { insert: r }, m: i }, a = 2) {
	a === 0 && r(e.targetAnchor, t, n);
	let { el: o, anchor: s, shapeFlag: c, children: l, props: u } = e, d = a === 2;
	if (d && r(o, t, n), !In.has(e) && (!d || zn(u)) && c & 16) for (let e = 0; e < l.length; e++) i(l[e], t, n, 2);
	d && r(s, t, n);
}
function Kn(e, t, n, r, i, a, { o: { nextSibling: o, parentNode: s, querySelector: c, insert: l, createText: u } }, d) {
	function f(e, n) {
		let r = n;
		for (; r;) {
			if (r && r.nodeType === 8) {
				if (r.data === "teleport start anchor") t.targetStart = r;
				else if (r.data === "teleport anchor") {
					t.targetAnchor = r, e._lpa = t.targetAnchor && o(t.targetAnchor);
					break;
				}
			}
			r = o(r);
		}
	}
	function p(e, t) {
		t.anchor = d(o(e), t, s(e), n, r, i, a);
	}
	let m = t.target = Un(t.props, c), h = zn(t.props);
	if (m) {
		let c = m._lpa || m.firstChild;
		t.shapeFlag & 16 && (h ? (p(e, t), f(m, c), t.targetAnchor || Yn(m, t, u, l, s(e) === m ? e : null)) : (t.anchor = o(e), f(m, c), t.targetAnchor || Yn(m, t, u, l), d(c && o(c), t, m, n, r, i, a))), Jn(t, h);
	} else h && t.shapeFlag & 16 && (p(e, t), t.targetStart = e, t.targetAnchor = o(e));
	return t.anchor && o(t.anchor);
}
var qn = Wn;
function Jn(e, t) {
	let n = e.ctx;
	if (n && n.ut) {
		let r, i;
		for (t ? (r = e.el, i = e.anchor) : (r = e.targetStart, i = e.targetAnchor); r && r !== i;) r.nodeType === 1 && r.setAttribute("data-v-owner", n.uid), r = r.nextSibling;
		n.ut();
	}
}
function Yn(e, t, n, r, i = null) {
	let a = t.targetStart = n(""), o = t.targetAnchor = n("");
	return a[Ln] = o, e && (r(a, e, i), r(o, e, i)), o;
}
var Xn = /* @__PURE__ */ Symbol("_leaveCb");
function Zn(e, t) {
	e.shapeFlag & 6 && e.component ? (e.transition = t, Zn(e.component.subTree, t)) : e.shapeFlag & 128 ? (e.ssContent.transition = t.clone(e.ssContent), e.ssFallback.transition = t.clone(e.ssFallback)) : e.transition = t;
}
// @__NO_SIDE_EFFECTS__
function Qn(e, t) {
	return h(e) ? /* @__PURE__ */ s({ name: e.name }, t, { setup: e }) : e;
}
function $n(e) {
	e.ids = [
		e.ids[0] + e.ids[2]++ + "-",
		0,
		0
	];
}
function er(e, t) {
	let n;
	return !!((n = Object.getOwnPropertyDescriptor(e, t)) && !n.configurable);
}
var tr = /* @__PURE__ */ new WeakMap();
function nr(e, n, r, a, o = !1) {
	if (d(e)) {
		e.forEach((e, t) => nr(e, n && (d(n) ? n[t] : n), r, a, o));
		return;
	}
	if (ir(a) && !o) {
		a.shapeFlag & 512 && a.type.__asyncResolved && a.component.subTree.component && nr(e, n, r, a.component.subTree);
		return;
	}
	let s = a.shapeFlag & 4 ? ka(a.component) : a.el, l = o ? null : s, { i: f, r: p } = e, m = n && n.r, _ = f.refs === t ? f.refs = {} : f.refs, v = f.setupState, y = /* @__PURE__ */ P(v), b = v === t ? i : (e) => er(_, e) ? !1 : u(y, e), x = (e, t) => !(t && er(_, t));
	if (m != null && m !== p) {
		if (rr(n), g(m)) _[m] = null, b(m) && (v[m] = null);
		else if (/* @__PURE__ */ Wt(m)) {
			let e = n;
			x(m, e.k) && (m.value = null), e.k && (_[e.k] = null);
		}
	}
	if (h(p)) nn(p, f, 12, [l, _]);
	else {
		let t = g(p), n = /* @__PURE__ */ Wt(p);
		if (t || n) {
			let i = () => {
				if (e.f) {
					let n = t ? b(p) ? v[p] : _[p] : x(p) || !e.k ? p.value : _[e.k];
					if (o) d(n) && c(n, s);
					else if (d(n)) n.includes(s) || n.push(s);
					else if (t) _[p] = [s], b(p) && (v[p] = _[p]);
					else {
						let t = [s];
						x(p, e.k) && (p.value = t), e.k && (_[e.k] = t);
					}
				} else t ? (_[p] = l, b(p) && (v[p] = l)) : n && (x(p, e.k) && (p.value = l), e.k && (_[e.k] = l));
			};
			if (l) {
				let t = () => {
					i(), tr.delete(e);
				};
				t.id = -1, tr.set(e, t), Ci(t, r);
			} else rr(e), i();
		}
	}
}
function rr(e) {
	let t = tr.get(e);
	t && (t.flags |= 8, tr.delete(e));
}
ce().requestIdleCallback, ce().cancelIdleCallback;
var ir = (e) => !!e.type.__asyncLoader, ar = (e) => e.type.__isKeepAlive;
function or(e, t) {
	cr(e, "a", t);
}
function sr(e, t) {
	cr(e, "da", t);
}
function cr(e, t, n = I) {
	let r = e.__wdc ||= () => {
		let t = n;
		for (; t;) {
			if (t.isDeactivated) return;
			t = t.parent;
		}
		return e();
	};
	if (ur(t, r, n), n) {
		let e = n.parent;
		for (; e && e.parent;) ar(e.parent.vnode) && lr(r, t, n, e), e = e.parent;
	}
}
function lr(e, t, n, r) {
	let i = ur(t, e, r, !0);
	_r(() => {
		c(r[t], i);
	}, n);
}
function ur(e, t, n = I, r = !1) {
	if (n) {
		let i = n[e] || (n[e] = []), a = t.__weh ||= (...r) => {
			He();
			let i = _a(n), a = rn(t, n, e, r);
			return i(), Ue(), a;
		};
		return r ? i.unshift(a) : i.push(a), a;
	}
}
var dr = (e) => (t, n = I) => {
	(!ba || e === "sp") && ur(e, (...e) => t(...e), n);
}, fr = dr("bm"), pr = dr("m"), mr = dr("bu"), hr = dr("u"), gr = dr("bum"), _r = dr("um"), vr = dr("sp"), yr = dr("rtg"), br = dr("rtc");
function xr(e, t = I) {
	ur("ec", e, t);
}
var Sr = /* @__PURE__ */ Symbol.for("v-ndc");
function Cr(e, t, n, r) {
	let i, a = n && n[r], o = d(e);
	if (o || g(e)) {
		let n = o && /* @__PURE__ */ Lt(e), r = !1, s = !1;
		n && (r = !/* @__PURE__ */ zt(e), s = /* @__PURE__ */ Rt(e), e = tt(e)), i = Array(e.length);
		for (let n = 0, o = e.length; n < o; n++) i[n] = t(r ? s ? Ut(Ht(e[n])) : Ht(e[n]) : e[n], n, void 0, a && a[n]);
	} else if (typeof e == "number") {
		i = Array(e);
		for (let n = 0; n < e; n++) i[n] = t(n + 1, n, void 0, a && a[n]);
	} else if (v(e)) if (e[Symbol.iterator]) i = Array.from(e, (e, n) => t(e, n, void 0, a && a[n]));
	else {
		let n = Object.keys(e);
		i = Array(n.length);
		for (let r = 0, o = n.length; r < o; r++) {
			let o = n[r];
			i[r] = t(e[o], o, r, a && a[r]);
		}
	}
	else i = [];
	return n && (n[r] = i), i;
}
var wr = (e) => e ? ya(e) ? ka(e) : wr(e.parent) : null, Tr = /* @__PURE__ */ s(/* @__PURE__ */ Object.create(null), {
	$: (e) => e,
	$el: (e) => e.vnode.el,
	$data: (e) => e.data,
	$props: (e) => e.props,
	$attrs: (e) => e.attrs,
	$slots: (e) => e.slots,
	$refs: (e) => e.refs,
	$parent: (e) => wr(e.parent),
	$root: (e) => wr(e.root),
	$host: (e) => e.ce,
	$emit: (e) => e.emit,
	$options: (e) => Pr(e),
	$forceUpdate: (e) => e.f ||= () => {
		gn(e.update);
	},
	$nextTick: (e) => e.n ||= mn.bind(e.proxy),
	$watch: (e) => Pn.bind(e)
}), Er = (e, n) => e !== t && !e.__isScriptSetup && u(e, n), Dr = {
	get({ _: e }, n) {
		if (n === "__v_skip") return !0;
		let { ctx: r, setupState: i, data: a, props: o, accessCache: s, type: c, appContext: l } = e;
		if (n[0] !== "$") {
			let e = s[n];
			if (e !== void 0) switch (e) {
				case 1: return i[n];
				case 2: return a[n];
				case 4: return r[n];
				case 3: return o[n];
			}
			else if (Er(i, n)) return s[n] = 1, i[n];
			else if (a !== t && u(a, n)) return s[n] = 2, a[n];
			else if (u(o, n)) return s[n] = 3, o[n];
			else if (r !== t && u(r, n)) return s[n] = 4, r[n];
			else kr && (s[n] = 0);
		}
		let d = Tr[n], f, p;
		if (d) return n === "$attrs" && N(e.attrs, "get", ""), d(e);
		if ((f = c.__cssModules) && (f = f[n])) return f;
		if (r !== t && u(r, n)) return s[n] = 4, r[n];
		if (p = l.config.globalProperties, u(p, n)) return p[n];
	},
	set({ _: e }, n, r) {
		let { data: i, setupState: a, ctx: o } = e;
		return Er(a, n) ? (a[n] = r, !0) : i !== t && u(i, n) ? (i[n] = r, !0) : u(e.props, n) || n[0] === "$" && n.slice(1) in e ? !1 : (o[n] = r, !0);
	},
	has({ _: { data: e, setupState: n, accessCache: r, ctx: i, appContext: a, props: o, type: s } }, c) {
		let l;
		return !!(r[c] || e !== t && c[0] !== "$" && u(e, c) || Er(n, c) || u(o, c) || u(i, c) || u(Tr, c) || u(a.config.globalProperties, c) || (l = s.__cssModules) && l[c]);
	},
	defineProperty(e, t, n) {
		return n.get == null ? u(n, "value") && this.set(e, t, n.value, null) : e._.accessCache[t] = 0, Reflect.defineProperty(e, t, n);
	}
};
function Or(e) {
	return d(e) ? e.reduce((e, t) => (e[t] = null, e), {}) : e;
}
var kr = !0;
function Ar(e) {
	let t = Pr(e), n = e.proxy, i = e.ctx;
	kr = !1, t.beforeCreate && Mr(t.beforeCreate, e, "bc");
	let { data: a, computed: o, methods: s, watch: c, provide: l, inject: u, created: f, beforeMount: p, mounted: m, beforeUpdate: g, updated: _, activated: y, deactivated: b, beforeDestroy: x, beforeUnmount: S, destroyed: C, unmounted: w, render: T, renderTracked: E, renderTriggered: D, errorCaptured: O, serverPrefetch: ee, expose: k, inheritAttrs: te, components: ne, directives: re, filters: ie } = t;
	if (u && jr(u, i, null), s) for (let e in s) {
		let t = s[e];
		h(t) && (i[e] = t.bind(n));
	}
	if (a) {
		let t = a.call(n, n);
		v(t) && (e.data = /* @__PURE__ */ Nt(t));
	}
	if (kr = !0, o) for (let e in o) {
		let t = o[e], a = ja({
			get: h(t) ? t.bind(n, n) : h(t.get) ? t.get.bind(n, n) : r,
			set: !h(t) && h(t.set) ? t.set.bind(n) : r
		});
		Object.defineProperty(i, e, {
			enumerable: !0,
			configurable: !0,
			get: () => a.value,
			set: (e) => a.value = e
		});
	}
	if (c) for (let e in c) Nr(c[e], i, n, e);
	if (l) {
		let e = h(l) ? l.call(n) : l;
		Reflect.ownKeys(e).forEach((t) => {
			On(t, e[t]);
		});
	}
	f && Mr(f, e, "c");
	function A(e, t) {
		d(t) ? t.forEach((t) => e(t.bind(n))) : t && e(t.bind(n));
	}
	if (A(fr, p), A(pr, m), A(mr, g), A(hr, _), A(or, y), A(sr, b), A(xr, O), A(br, E), A(yr, D), A(gr, S), A(_r, w), A(vr, ee), d(k)) if (k.length) {
		let t = e.exposed ||= {};
		k.forEach((e) => {
			Object.defineProperty(t, e, {
				get: () => n[e],
				set: (t) => n[e] = t,
				enumerable: !0
			});
		});
	} else e.exposed ||= {};
	T && e.render === r && (e.render = T), te != null && (e.inheritAttrs = te), ne && (e.components = ne), re && (e.directives = re), ee && $n(e);
}
function jr(e, t, n = r) {
	d(e) && (e = zr(e));
	for (let n in e) {
		let r = e[n], i;
		i = v(r) ? "default" in r ? kn(r.from || n, r.default, !0) : kn(r.from || n) : kn(r), /* @__PURE__ */ Wt(i) ? Object.defineProperty(t, n, {
			enumerable: !0,
			configurable: !0,
			get: () => i.value,
			set: (e) => i.value = e
		}) : t[n] = i;
	}
}
function Mr(e, t, n) {
	rn(d(e) ? e.map((e) => e.bind(t.proxy)) : e.bind(t.proxy), t, n);
}
function Nr(e, t, n, r) {
	let i = r.includes(".") ? Fn(n, r) : () => n[r];
	if (g(e)) {
		let n = t[e];
		h(n) && Mn(i, n);
	} else if (h(e)) Mn(i, e.bind(n));
	else if (v(e)) if (d(e)) e.forEach((e) => Nr(e, t, n, r));
	else {
		let r = h(e.handler) ? e.handler.bind(n) : t[e.handler];
		h(r) && Mn(i, r, e);
	}
}
function Pr(e) {
	let t = e.type, { mixins: n, extends: r } = t, { mixins: i, optionsCache: a, config: { optionMergeStrategies: o } } = e.appContext, s = a.get(t), c;
	return s ? c = s : !i.length && !n && !r ? c = t : (c = {}, i.length && i.forEach((e) => Fr(c, e, o, !0)), Fr(c, t, o)), v(t) && a.set(t, c), c;
}
function Fr(e, t, n, r = !1) {
	let { mixins: i, extends: a } = t;
	a && Fr(e, a, n, !0), i && i.forEach((t) => Fr(e, t, n, !0));
	for (let i in t) if (!(r && i === "expose")) {
		let r = Ir[i] || n && n[i];
		e[i] = r ? r(e[i], t[i]) : t[i];
	}
	return e;
}
var Ir = {
	data: Lr,
	props: Vr,
	emits: Vr,
	methods: Br,
	computed: Br,
	beforeCreate: F,
	created: F,
	beforeMount: F,
	mounted: F,
	beforeUpdate: F,
	updated: F,
	beforeDestroy: F,
	beforeUnmount: F,
	destroyed: F,
	unmounted: F,
	activated: F,
	deactivated: F,
	errorCaptured: F,
	serverPrefetch: F,
	components: Br,
	directives: Br,
	watch: Hr,
	provide: Lr,
	inject: Rr
};
function Lr(e, t) {
	return t ? e ? function() {
		return s(h(e) ? e.call(this, this) : e, h(t) ? t.call(this, this) : t);
	} : t : e;
}
function Rr(e, t) {
	return Br(zr(e), zr(t));
}
function zr(e) {
	if (d(e)) {
		let t = {};
		for (let n = 0; n < e.length; n++) t[e[n]] = e[n];
		return t;
	}
	return e;
}
function F(e, t) {
	return e ? [...new Set([].concat(e, t))] : t;
}
function Br(e, t) {
	return e ? s(/* @__PURE__ */ Object.create(null), e, t) : t;
}
function Vr(e, t) {
	return e ? d(e) && d(t) ? [.../* @__PURE__ */ new Set([...e, ...t])] : s(/* @__PURE__ */ Object.create(null), Or(e), Or(t ?? {})) : t;
}
function Hr(e, t) {
	if (!e) return t;
	if (!t) return e;
	let n = s(/* @__PURE__ */ Object.create(null), e);
	for (let r in t) n[r] = F(e[r], t[r]);
	return n;
}
function Ur() {
	return {
		app: null,
		config: {
			isNativeTag: i,
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
var Wr = 0;
function Gr(e, t) {
	return function(n, r = null) {
		h(n) || (n = s({}, n)), r != null && !v(r) && (r = null);
		let i = Ur(), a = /* @__PURE__ */ new WeakSet(), o = [], c = !1, l = i.app = {
			_uid: Wr++,
			_component: n,
			_props: r,
			_container: null,
			_context: i,
			_instance: null,
			version: Ma,
			get config() {
				return i.config;
			},
			set config(e) {},
			use(e, ...t) {
				return a.has(e) || (e && h(e.install) ? (a.add(e), e.install(l, ...t)) : h(e) && (a.add(e), e(l, ...t))), l;
			},
			mixin(e) {
				return i.mixins.includes(e) || i.mixins.push(e), l;
			},
			component(e, t) {
				return t ? (i.components[e] = t, l) : i.components[e];
			},
			directive(e, t) {
				return t ? (i.directives[e] = t, l) : i.directives[e];
			},
			mount(a, o, s) {
				if (!c) {
					let u = l._ceVNode || ea(n, r);
					return u.appContext = i, s === !0 ? s = "svg" : s === !1 && (s = void 0), o && t ? t(u, a) : e(u, a, s), c = !0, l._container = a, a.__vue_app__ = l, ka(u.component);
				}
			},
			onUnmount(e) {
				o.push(e);
			},
			unmount() {
				c && (rn(o, l._instance, 16), e(null, l._container), delete l._container.__vue_app__);
			},
			provide(e, t) {
				return i.provides[e] = t, l;
			},
			runWithContext(e) {
				let t = Kr;
				Kr = l;
				try {
					return e();
				} finally {
					Kr = t;
				}
			}
		};
		return l;
	};
}
var Kr = null, qr = (e, t) => t === "modelValue" || t === "model-value" ? e.modelModifiers : e[`${t}Modifiers`] || e[`${O(t)}Modifiers`] || e[`${k(t)}Modifiers`];
function Jr(e, n, ...r) {
	if (e.isUnmounted) return;
	let i = e.vnode.props || t, a = r, o = n.startsWith("update:"), s = o && qr(i, n.slice(7));
	s && (s.trim && (a = r.map((e) => g(e) ? e.trim() : e)), s.number && (a = r.map(ae)));
	let c, l = i[c = ne(n)] || i[c = ne(O(n))];
	!l && o && (l = i[c = ne(k(n))]), l && rn(l, e, 6, a);
	let u = i[c + "Once"];
	if (u) {
		if (!e.emitted) e.emitted = {};
		else if (e.emitted[c]) return;
		e.emitted[c] = !0, rn(u, e, 6, a);
	}
}
var Yr = /* @__PURE__ */ new WeakMap();
function Xr(e, t, n = !1) {
	let r = n ? Yr : t.emitsCache, i = r.get(e);
	if (i !== void 0) return i;
	let a = e.emits, o = {}, c = !1;
	if (!h(e)) {
		let r = (e) => {
			let n = Xr(e, t, !0);
			n && (c = !0, s(o, n));
		};
		!n && t.mixins.length && t.mixins.forEach(r), e.extends && r(e.extends), e.mixins && e.mixins.forEach(r);
	}
	return !a && !c ? (v(e) && r.set(e, null), null) : (d(a) ? a.forEach((e) => o[e] = null) : s(o, a), v(e) && r.set(e, o), o);
}
function Zr(e, t) {
	return !e || !a(t) ? !1 : (t = t.slice(2).replace(/Once$/, ""), u(e, t[0].toLowerCase() + t.slice(1)) || u(e, k(t)) || u(e, t));
}
function Qr(e) {
	let { type: t, vnode: n, proxy: r, withProxy: i, propsOptions: [a], slots: s, attrs: c, emit: l, render: u, renderCache: d, props: f, data: p, setupState: m, ctx: h, inheritAttrs: g } = e, _ = Tn(e), v, y;
	try {
		if (n.shapeFlag & 4) {
			let e = i || r, t = e;
			v = oa(u.call(t, e, d, f, m, p, h)), y = c;
		} else {
			let e = t;
			v = oa(e.length > 1 ? e(f, {
				attrs: c,
				slots: s,
				emit: l
			}) : e(f, null)), y = t.props ? c : $r(c);
		}
	} catch (t) {
		Bi.length = 0, an(t, e, 1), v = ea(Ri);
	}
	let b = v;
	if (y && g !== !1) {
		let e = Object.keys(y), { shapeFlag: t } = b;
		e.length && t & 7 && (a && e.some(o) && (y = ei(y, a)), b = ra(b, y, !1, !0));
	}
	return n.dirs && (b = ra(b, null, !1, !0), b.dirs = b.dirs ? b.dirs.concat(n.dirs) : n.dirs), n.transition && Zn(b, n.transition), v = b, Tn(_), v;
}
var $r = (e) => {
	let t;
	for (let n in e) (n === "class" || n === "style" || a(n)) && ((t ||= {})[n] = e[n]);
	return t;
}, ei = (e, t) => {
	let n = {};
	for (let r in e) (!o(r) || !(r.slice(9) in t)) && (n[r] = e[r]);
	return n;
};
function ti(e, t, n) {
	let { props: r, children: i, component: a } = e, { props: o, children: s, patchFlag: c } = t, l = a.emitsOptions;
	if (t.dirs || t.transition) return !0;
	if (n && c >= 0) {
		if (c & 1024) return !0;
		if (c & 16) return r ? ni(r, o, l) : !!o;
		if (c & 8) {
			let e = t.dynamicProps;
			for (let t = 0; t < e.length; t++) {
				let n = e[t];
				if (ri(o, r, n) && !Zr(l, n)) return !0;
			}
		}
	} else return (i || s) && (!s || !s.$stable) ? !0 : r === o ? !1 : r ? o ? ni(r, o, l) : !0 : !!o;
	return !1;
}
function ni(e, t, n) {
	let r = Object.keys(t);
	if (r.length !== Object.keys(e).length) return !0;
	for (let i = 0; i < r.length; i++) {
		let a = r[i];
		if (ri(t, e, a) && !Zr(n, a)) return !0;
	}
	return !1;
}
function ri(e, t, n) {
	let r = e[n], i = t[n];
	return n === "style" && v(r) && v(i) ? !ye(r, i) : r !== i;
}
function ii({ vnode: e, parent: t, suspense: n }, r) {
	for (; t;) {
		let n = t.subTree;
		if (n.suspense && n.suspense.activeBranch === e && (n.suspense.vnode.el = n.el = r, e = n), n === e) (e = t.vnode).el = r, t = t.parent;
		else break;
	}
	n && n.activeBranch === e && (n.vnode.el = r);
}
var ai = {}, oi = () => Object.create(ai), si = (e) => Object.getPrototypeOf(e) === ai;
function ci(e, t, n, r = !1) {
	let i = {}, a = oi();
	e.propsDefaults = /* @__PURE__ */ Object.create(null), ui(e, t, i, a);
	for (let t in e.propsOptions[0]) t in i || (i[t] = void 0);
	n ? e.props = r ? i : /* @__PURE__ */ Pt(i) : e.type.props ? e.props = i : e.props = a, e.attrs = a;
}
function li(e, t, n, r) {
	let { props: i, attrs: a, vnode: { patchFlag: o } } = e, s = /* @__PURE__ */ P(i), [c] = e.propsOptions, l = !1;
	if ((r || o > 0) && !(o & 16)) {
		if (o & 8) {
			let n = e.vnode.dynamicProps;
			for (let r = 0; r < n.length; r++) {
				let o = n[r];
				if (Zr(e.emitsOptions, o)) continue;
				let d = t[o];
				if (c) if (u(a, o)) d !== a[o] && (a[o] = d, l = !0);
				else {
					let t = O(o);
					i[t] = di(c, s, t, d, e, !1);
				}
				else d !== a[o] && (a[o] = d, l = !0);
			}
		}
	} else {
		ui(e, t, i, a) && (l = !0);
		let r;
		for (let a in s) (!t || !u(t, a) && ((r = k(a)) === a || !u(t, r))) && (c ? n && (n[a] !== void 0 || n[r] !== void 0) && (i[a] = di(c, s, a, void 0, e, !0)) : delete i[a]);
		if (a !== s) for (let e in a) (!t || !u(t, e)) && (delete a[e], l = !0);
	}
	l && $e(e.attrs, "set", "");
}
function ui(e, n, r, i) {
	let [a, o] = e.propsOptions, s = !1, c;
	if (n) for (let t in n) {
		if (T(t)) continue;
		let l = n[t], d;
		a && u(a, d = O(t)) ? !o || !o.includes(d) ? r[d] = l : (c ||= {})[d] = l : Zr(e.emitsOptions, t) || (!(t in i) || l !== i[t]) && (i[t] = l, s = !0);
	}
	if (o) {
		let n = /* @__PURE__ */ P(r), i = c || t;
		for (let t = 0; t < o.length; t++) {
			let s = o[t];
			r[s] = di(a, n, s, i[s], e, !u(i, s));
		}
	}
	return s;
}
function di(e, t, n, r, i, a) {
	let o = e[n];
	if (o != null) {
		let e = u(o, "default");
		if (e && r === void 0) {
			let e = o.default;
			if (o.type !== Function && !o.skipFactory && h(e)) {
				let { propsDefaults: a } = i;
				if (n in a) r = a[n];
				else {
					let o = _a(i);
					r = a[n] = e.call(null, t), o();
				}
			} else r = e;
			i.ce && i.ce._setProp(n, r);
		}
		o[0] && (a && !e ? r = !1 : o[1] && (r === "" || r === k(n)) && (r = !0));
	}
	return r;
}
var fi = /* @__PURE__ */ new WeakMap();
function pi(e, r, i = !1) {
	let a = i ? fi : r.propsCache, o = a.get(e);
	if (o) return o;
	let c = e.props, l = {}, f = [], p = !1;
	if (!h(e)) {
		let t = (e) => {
			p = !0;
			let [t, n] = pi(e, r, !0);
			s(l, t), n && f.push(...n);
		};
		!i && r.mixins.length && r.mixins.forEach(t), e.extends && t(e.extends), e.mixins && e.mixins.forEach(t);
	}
	if (!c && !p) return v(e) && a.set(e, n), n;
	if (d(c)) for (let e = 0; e < c.length; e++) {
		let n = O(c[e]);
		mi(n) && (l[n] = t);
	}
	else if (c) for (let e in c) {
		let t = O(e);
		if (mi(t)) {
			let n = c[e], r = l[t] = d(n) || h(n) ? { type: n } : s({}, n), i = r.type, a = !1, o = !0;
			if (d(i)) for (let e = 0; e < i.length; ++e) {
				let t = i[e], n = h(t) && t.name;
				if (n === "Boolean") {
					a = !0;
					break;
				} else n === "String" && (o = !1);
			}
			else a = h(i) && i.name === "Boolean";
			r[0] = a, r[1] = o, (a || u(r, "default")) && f.push(t);
		}
	}
	let m = [l, f];
	return v(e) && a.set(e, m), m;
}
function mi(e) {
	return e[0] !== "$" && !T(e);
}
var hi = (e) => e === "_" || e === "_ctx" || e === "$stable", gi = (e) => d(e) ? e.map(oa) : [oa(e)], _i = (e, t, n) => {
	if (t._n) return t;
	let r = En((...e) => gi(t(...e)), n);
	return r._c = !1, r;
}, vi = (e, t, n) => {
	let r = e._ctx;
	for (let n in e) {
		if (hi(n)) continue;
		let i = e[n];
		if (h(i)) t[n] = _i(n, i, r);
		else if (i != null) {
			let e = gi(i);
			t[n] = () => e;
		}
	}
}, yi = (e, t) => {
	let n = gi(t);
	e.slots.default = () => n;
}, bi = (e, t, n) => {
	for (let r in t) (n || !hi(r)) && (e[r] = t[r]);
}, xi = (e, t, n) => {
	let r = e.slots = oi();
	if (e.vnode.shapeFlag & 32) {
		let e = t._;
		e ? (bi(r, t, n), n && A(r, "_", e, !0)) : vi(t, r);
	} else t && yi(e, t);
}, Si = (e, n, r) => {
	let { vnode: i, slots: a } = e, o = !0, s = t;
	if (i.shapeFlag & 32) {
		let e = n._;
		e ? r && e === 1 ? o = !1 : bi(a, n, r) : (o = !n.$stable, vi(n, a)), s = n;
	} else n && (yi(e, n), s = { default: 1 });
	if (o) for (let e in a) !hi(e) && s[e] == null && delete a[e];
}, Ci = Fi;
function wi(e) {
	return Ti(e);
}
function Ti(e, i) {
	let a = ce();
	a.__VUE__ = !0;
	let { insert: o, remove: s, patchProp: c, createElement: l, createText: u, createComment: d, setText: f, setElementText: p, parentNode: m, nextSibling: h, setScopeId: g = r, insertStaticContent: _ } = e, v = (e, t, n, r = null, i = null, a = null, o = void 0, s = null, c = !!t.dynamicChildren) => {
		if (e === t) return;
		e && !Xi(e, t) && (r = ve(e), pe(e, i, a, !0), e = null), t.patchFlag === -2 && (c = !1, t.dynamicChildren = null);
		let { type: l, ref: u, shapeFlag: d } = t;
		switch (l) {
			case Li:
				y(e, t, n, r);
				break;
			case Ri:
				b(e, t, n, r);
				break;
			case zi:
				e ?? x(t, n, r, o);
				break;
			case Ii:
				ne(e, t, n, r, i, a, o, s, c);
				break;
			default: d & 1 ? w(e, t, n, r, i, a, o, s, c) : d & 6 ? re(e, t, n, r, i, a, o, s, c) : (d & 64 || d & 128) && l.process(e, t, n, r, i, a, o, s, c, xe);
		}
		u != null && i ? nr(u, e && e.ref, a, t || e, !t) : u == null && e && e.ref != null && nr(e.ref, null, a, e, !0);
	}, y = (e, t, n, r) => {
		if (e == null) o(t.el = u(t.children), n, r);
		else {
			let n = t.el = e.el;
			t.children !== e.children && f(n, t.children);
		}
	}, b = (e, t, n, r) => {
		e == null ? o(t.el = d(t.children || ""), n, r) : t.el = e.el;
	}, x = (e, t, n, r) => {
		[e.el, e.anchor] = _(e.children, t, n, r, e.el, e.anchor);
	}, S = ({ el: e, anchor: t }, n, r) => {
		let i;
		for (; e && e !== t;) i = h(e), o(e, n, r), e = i;
		o(t, n, r);
	}, C = ({ el: e, anchor: t }) => {
		let n;
		for (; e && e !== t;) n = h(e), s(e), e = n;
		s(t);
	}, w = (e, t, n, r, i, a, o, s, c) => {
		if (t.type === "svg" ? o = "svg" : t.type === "math" && (o = "mathml"), e == null) E(t, n, r, i, a, o, s, c);
		else {
			let n = e.el && e.el._isVueCE ? e.el : null;
			try {
				n && n._beginPatch(), ee(e, t, i, a, o, s, c);
			} finally {
				n && n._endPatch();
			}
		}
	}, E = (e, t, n, r, i, a, s, u) => {
		let d, f, { props: m, shapeFlag: h, transition: g, dirs: _ } = e;
		if (d = e.el = l(e.type, a, m && m.is, m), h & 8 ? p(d, e.children) : h & 16 && O(e.children, d, null, r, i, Ei(e, a), s, u), _ && Dn(e, null, r, "created"), D(d, e, e.scopeId, s, r), m) {
			for (let e in m) e !== "value" && !T(e) && c(d, e, null, m[e], a, r);
			"value" in m && c(d, "value", null, m.value, a), (f = m.onVnodeBeforeMount) && ua(f, r, e);
		}
		_ && Dn(e, null, r, "beforeMount");
		let v = Oi(i, g);
		v && g.beforeEnter(d), o(d, t, n), ((f = m && m.onVnodeMounted) || v || _) && Ci(() => {
			try {
				f && ua(f, r, e), v && g.enter(d), _ && Dn(e, null, r, "mounted");
			} finally {}
		}, i);
	}, D = (e, t, n, r, i) => {
		if (n && g(e, n), r) for (let t = 0; t < r.length; t++) g(e, r[t]);
		if (i) {
			let n = i.subTree;
			if (t === n || Pi(n.type) && (n.ssContent === t || n.ssFallback === t)) {
				let t = i.vnode;
				D(e, t, t.scopeId, t.slotScopeIds, i.parent);
			}
		}
	}, O = (e, t, n, r, i, a, o, s, c = 0) => {
		for (let l = c; l < e.length; l++) v(null, e[l] = s ? sa(e[l]) : oa(e[l]), t, n, r, i, a, o, s);
	}, ee = (e, n, r, i, a, o, s) => {
		let l = n.el = e.el, { patchFlag: u, dynamicChildren: d, dirs: f } = n;
		u |= e.patchFlag & 16;
		let m = e.props || t, h = n.props || t, g;
		if (r && Di(r, !1), (g = h.onVnodeBeforeUpdate) && ua(g, r, n, e), f && Dn(n, e, r, "beforeUpdate"), r && Di(r, !0), (m.innerHTML && h.innerHTML == null || m.textContent && h.textContent == null) && p(l, ""), d ? k(e.dynamicChildren, d, l, r, i, Ei(n, a), o) : s || le(e, n, l, null, r, i, Ei(n, a), o, !1), u > 0) {
			if (u & 16) te(l, m, h, r, a);
			else if (u & 2 && m.class !== h.class && c(l, "class", null, h.class, a), u & 4 && c(l, "style", m.style, h.style, a), u & 8) {
				let e = n.dynamicProps;
				for (let t = 0; t < e.length; t++) {
					let n = e[t], i = m[n], o = h[n];
					(o !== i || n === "value") && c(l, n, i, o, a, r);
				}
			}
			u & 1 && e.children !== n.children && p(l, n.children);
		} else !s && d == null && te(l, m, h, r, a);
		((g = h.onVnodeUpdated) || f) && Ci(() => {
			g && ua(g, r, n, e), f && Dn(n, e, r, "updated");
		}, i);
	}, k = (e, t, n, r, i, a, o) => {
		for (let s = 0; s < t.length; s++) {
			let c = e[s], l = t[s];
			v(c, l, c.el && (c.type === Ii || !Xi(c, l) || c.shapeFlag & 198) ? m(c.el) : n, null, r, i, a, o, !0);
		}
	}, te = (e, n, r, i, a) => {
		if (n !== r) {
			if (n !== t) for (let t in n) !T(t) && !(t in r) && c(e, t, n[t], null, a, i);
			for (let t in r) {
				if (T(t)) continue;
				let o = r[t], s = n[t];
				o !== s && t !== "value" && c(e, t, s, o, a, i);
			}
			"value" in r && c(e, "value", n.value, r.value, a);
		}
	}, ne = (e, t, n, r, i, a, s, c, l) => {
		let d = t.el = e ? e.el : u(""), f = t.anchor = e ? e.anchor : u(""), { patchFlag: p, dynamicChildren: m, slotScopeIds: h } = t;
		h && (c = c ? c.concat(h) : h), e == null ? (o(d, n, r), o(f, n, r), O(t.children || [], n, f, i, a, s, c, l)) : p > 0 && p & 64 && m && e.dynamicChildren && e.dynamicChildren.length === m.length ? (k(e.dynamicChildren, m, n, i, a, s, c), (t.key != null || i && t === i.subTree) && ki(e, t, !0)) : le(e, t, n, f, i, a, s, c, l);
	}, re = (e, t, n, r, i, a, o, s, c) => {
		t.slotScopeIds = s, e == null ? t.shapeFlag & 512 ? i.ctx.activate(t, n, r, o, c) : A(t, n, r, i, a, o, c) : ae(e, t, c);
	}, A = (e, t, n, r, i, a, o) => {
		let s = e.component = pa(e, r, i);
		if (ar(e) && (s.ctx.renderer = xe), xa(s, !1, o), s.asyncDep) {
			if (i && i.registerDep(s, oe, o), !e.el) {
				let r = s.subTree = ea(Ri);
				b(null, r, t, n), e.placeholder = r.el;
			}
		} else oe(s, e, t, n, i, a, o);
	}, ae = (e, t, n) => {
		let r = t.component = e.component;
		if (ti(e, t, n)) if (r.asyncDep && !r.asyncResolved) {
			se(r, t, n);
			return;
		} else r.next = t, r.update();
		else t.el = e.el, r.vnode = t;
	}, oe = (e, t, n, r, i, a, o) => {
		let s = () => {
			if (e.isMounted) {
				let { next: t, bu: n, u: r, parent: s, vnode: c } = e;
				{
					let n = ji(e);
					if (n) {
						t && (t.el = c.el, se(e, t, o)), n.asyncDep.then(() => {
							Ci(() => {
								e.isUnmounted || l();
							}, i);
						});
						return;
					}
				}
				let u = t, d;
				Di(e, !1), t ? (t.el = c.el, se(e, t, o)) : t = c, n && ie(n), (d = t.props && t.props.onVnodeBeforeUpdate) && ua(d, s, t, c), Di(e, !0);
				let f = Qr(e), p = e.subTree;
				e.subTree = f, v(p, f, m(p.el), ve(p), e, i, a), t.el = f.el, u === null && ii(e, f.el), r && Ci(r, i), (d = t.props && t.props.onVnodeUpdated) && Ci(() => ua(d, s, t, c), i);
			} else {
				let o, { el: s, props: c } = t, { bm: l, m: u, parent: d, root: f, type: p } = e, m = ir(t);
				if (Di(e, !1), l && ie(l), !m && (o = c && c.onVnodeBeforeMount) && ua(o, d, t), Di(e, !0), s && Ce) {
					let t = () => {
						e.subTree = Qr(e), Ce(s, e.subTree, e, i, null);
					};
					m && p.__asyncHydrate ? p.__asyncHydrate(s, e, t) : t();
				} else {
					f.ce && f.ce._hasShadowRoot() && f.ce._injectChildStyle(p, e.parent ? e.parent.type : void 0);
					let o = e.subTree = Qr(e);
					v(null, o, n, r, e, i, a), t.el = o.el;
				}
				if (u && Ci(u, i), !m && (o = c && c.onVnodeMounted)) {
					let e = t;
					Ci(() => ua(o, d, e), i);
				}
				(t.shapeFlag & 256 || d && ir(d.vnode) && d.vnode.shapeFlag & 256) && e.a && Ci(e.a, i), e.isMounted = !0, t = n = r = null;
			}
		};
		e.scope.on();
		let c = e.effect = new De(s);
		e.scope.off();
		let l = e.update = c.run.bind(c), u = e.job = c.runIfDirty.bind(c);
		u.i = e, u.id = e.uid, c.scheduler = () => gn(u), Di(e, !0), l();
	}, se = (e, t, n) => {
		t.component = e;
		let r = e.vnode.props;
		e.vnode = t, e.next = null, li(e, t.props, r, n), Si(e, t.children, n), He(), yn(e), Ue();
	}, le = (e, t, n, r, i, a, o, s, c = !1) => {
		let l = e && e.children, u = e ? e.shapeFlag : 0, d = t.children, { patchFlag: f, shapeFlag: m } = t;
		if (f > 0) {
			if (f & 128) {
				de(l, d, n, r, i, a, o, s, c);
				return;
			} else if (f & 256) {
				ue(l, d, n, r, i, a, o, s, c);
				return;
			}
		}
		m & 8 ? (u & 16 && _e(l, i, a), d !== l && p(n, d)) : u & 16 ? m & 16 ? de(l, d, n, r, i, a, o, s, c) : _e(l, i, a, !0) : (u & 8 && p(n, ""), m & 16 && O(d, n, r, i, a, o, s, c));
	}, ue = (e, t, r, i, a, o, s, c, l) => {
		e ||= n, t ||= n;
		let u = e.length, d = t.length, f = Math.min(u, d), p;
		for (p = 0; p < f; p++) {
			let n = t[p] = l ? sa(t[p]) : oa(t[p]);
			v(e[p], n, r, null, a, o, s, c, l);
		}
		u > d ? _e(e, a, o, !0, !1, f) : O(t, r, i, a, o, s, c, l, f);
	}, de = (e, t, r, i, a, o, s, c, l) => {
		let u = 0, d = t.length, f = e.length - 1, p = d - 1;
		for (; u <= f && u <= p;) {
			let n = e[u], i = t[u] = l ? sa(t[u]) : oa(t[u]);
			if (Xi(n, i)) v(n, i, r, null, a, o, s, c, l);
			else break;
			u++;
		}
		for (; u <= f && u <= p;) {
			let n = e[f], i = t[p] = l ? sa(t[p]) : oa(t[p]);
			if (Xi(n, i)) v(n, i, r, null, a, o, s, c, l);
			else break;
			f--, p--;
		}
		if (u > f) {
			if (u <= p) {
				let e = p + 1, n = e < d ? t[e].el : i;
				for (; u <= p;) v(null, t[u] = l ? sa(t[u]) : oa(t[u]), r, n, a, o, s, c, l), u++;
			}
		} else if (u > p) for (; u <= f;) pe(e[u], a, o, !0), u++;
		else {
			let m = u, h = u, g = /* @__PURE__ */ new Map();
			for (u = h; u <= p; u++) {
				let e = t[u] = l ? sa(t[u]) : oa(t[u]);
				e.key != null && g.set(e.key, u);
			}
			let _, y = 0, b = p - h + 1, x = !1, S = 0, C = Array(b);
			for (u = 0; u < b; u++) C[u] = 0;
			for (u = m; u <= f; u++) {
				let n = e[u];
				if (y >= b) {
					pe(n, a, o, !0);
					continue;
				}
				let i;
				if (n.key != null) i = g.get(n.key);
				else for (_ = h; _ <= p; _++) if (C[_ - h] === 0 && Xi(n, t[_])) {
					i = _;
					break;
				}
				i === void 0 ? pe(n, a, o, !0) : (C[i - h] = u + 1, i >= S ? S = i : x = !0, v(n, t[i], r, null, a, o, s, c, l), y++);
			}
			let w = x ? Ai(C) : n;
			for (_ = w.length - 1, u = b - 1; u >= 0; u--) {
				let e = h + u, n = t[e], f = t[e + 1], p = e + 1 < d ? f.el || Ni(f) : i;
				C[u] === 0 ? v(null, n, r, p, a, o, s, c, l) : x && (_ < 0 || u !== w[_] ? fe(n, r, p, 2) : _--);
			}
		}
	}, fe = (e, t, n, r, i = null) => {
		let { el: a, type: c, transition: l, children: u, shapeFlag: d } = e;
		if (d & 6) {
			fe(e.component.subTree, t, n, r);
			return;
		}
		if (d & 128) {
			e.suspense.move(t, n, r);
			return;
		}
		if (d & 64) {
			c.move(e, t, n, xe);
			return;
		}
		if (c === Ii) {
			o(a, t, n);
			for (let e = 0; e < u.length; e++) fe(u[e], t, n, r);
			o(e.anchor, t, n);
			return;
		}
		if (c === zi) {
			S(e, t, n);
			return;
		}
		if (r !== 2 && d & 1 && l) if (r === 0) l.persisted && !a[Xn] ? o(a, t, n) : (l.beforeEnter(a), o(a, t, n), Ci(() => l.enter(a), i));
		else {
			let { leave: r, delayLeave: i, afterLeave: c } = l, u = () => {
				e.ctx.isUnmounted ? s(a) : o(a, t, n);
			}, d = () => {
				let e = a._isLeaving || !!a[Xn];
				a._isLeaving && a[Xn](!0), l.persisted && !e ? u() : r(a, () => {
					u(), c && c();
				});
			};
			i ? i(a, u, d) : d();
		}
		else o(a, t, n);
	}, pe = (e, t, n, r = !1, i = !1) => {
		let { type: a, props: o, ref: s, children: c, dynamicChildren: l, shapeFlag: u, patchFlag: d, dirs: f, cacheIndex: p, memo: m } = e;
		if (d === -2 && (i = !1), s != null && (He(), nr(s, null, n, e, !0), Ue()), p != null && (t.renderCache[p] = void 0), u & 256) {
			t.ctx.deactivate(e);
			return;
		}
		let h = u & 1 && f, g = !ir(e), _;
		if (g && (_ = o && o.onVnodeBeforeUnmount) && ua(_, t, e), u & 6) ge(e.component, n, r);
		else {
			if (u & 128) {
				e.suspense.unmount(n, r);
				return;
			}
			h && Dn(e, null, t, "beforeUnmount"), u & 64 ? e.type.remove(e, t, n, xe, r) : l && !l.hasOnce && (a !== Ii || d > 0 && d & 64) ? _e(l, t, n, !1, !0) : (a === Ii && d & 384 || !i && u & 16) && _e(c, t, n), r && me(e);
		}
		let v = m != null && p == null;
		(g && (_ = o && o.onVnodeUnmounted) || h || v) && Ci(() => {
			_ && ua(_, t, e), h && Dn(e, null, t, "unmounted"), v && (e.el = null);
		}, n);
	}, me = (e) => {
		let { type: t, el: n, anchor: r, transition: i } = e;
		if (t === Ii) {
			he(n, r);
			return;
		}
		if (t === zi) {
			C(e);
			return;
		}
		let a = () => {
			s(n), i && !i.persisted && i.afterLeave && i.afterLeave();
		};
		if (e.shapeFlag & 1 && i && !i.persisted) {
			let { leave: t, delayLeave: r } = i, o = () => t(n, a);
			r ? r(e.el, a, o) : o();
		} else a();
	}, he = (e, t) => {
		let n;
		for (; e !== t;) n = h(e), s(e), e = n;
		s(t);
	}, ge = (e, t, n) => {
		let { bum: r, scope: i, job: a, subTree: o, um: s, m: c, a: l } = e;
		Mi(c), Mi(l), r && ie(r), i.stop(), a && (a.flags |= 8, pe(o, e, t, n)), s && Ci(s, t), Ci(() => {
			e.isUnmounted = !0;
		}, t);
	}, _e = (e, t, n, r = !1, i = !1, a = 0) => {
		for (let o = a; o < e.length; o++) pe(e[o], t, n, r, i);
	}, ve = (e) => {
		if (e.shapeFlag & 6) return ve(e.component.subTree);
		if (e.shapeFlag & 128) return e.suspense.next();
		let t = h(e.anchor || e.el), n = t && t[Ln];
		return n ? h(n) : t;
	}, ye = !1, be = (e, t, n) => {
		let r;
		e == null ? t._vnode && (pe(t._vnode, null, null, !0), r = t._vnode.component) : v(t._vnode || null, e, t, null, null, null, n), t._vnode = e, ye ||= (ye = !0, yn(r), bn(), !1);
	}, xe = {
		p: v,
		um: pe,
		m: fe,
		r: me,
		mt: A,
		mc: O,
		pc: le,
		pbc: k,
		n: ve,
		o: e
	}, Se, Ce;
	return i && ([Se, Ce] = i(xe)), {
		render: be,
		hydrate: Se,
		createApp: Gr(be, Se)
	};
}
function Ei({ type: e, props: t }, n) {
	return n === "svg" && e === "foreignObject" || n === "mathml" && e === "annotation-xml" && t && t.encoding && t.encoding.includes("html") ? void 0 : n;
}
function Di({ effect: e, job: t }, n) {
	n ? (e.flags |= 32, t.flags |= 4) : (e.flags &= -33, t.flags &= -5);
}
function Oi(e, t) {
	return (!e || e && !e.pendingBranch) && t && !t.persisted;
}
function ki(e, t, n = !1) {
	let r = e.children, i = t.children;
	if (d(r) && d(i)) for (let e = 0; e < r.length; e++) {
		let t = r[e], a = i[e];
		a.shapeFlag & 1 && !a.dynamicChildren && ((a.patchFlag <= 0 || a.patchFlag === 32) && (a = i[e] = sa(i[e]), a.el = t.el), !n && a.patchFlag !== -2 && ki(t, a)), a.type === Li && (a.patchFlag === -1 && (a = i[e] = sa(a)), a.el = t.el), a.type === Ri && !a.el && (a.el = t.el);
	}
}
function Ai(e) {
	let t = e.slice(), n = [0], r, i, a, o, s, c = e.length;
	for (r = 0; r < c; r++) {
		let c = e[r];
		if (c !== 0) {
			if (i = n[n.length - 1], e[i] < c) {
				t[r] = i, n.push(r);
				continue;
			}
			for (a = 0, o = n.length - 1; a < o;) s = a + o >> 1, e[n[s]] < c ? a = s + 1 : o = s;
			c < e[n[a]] && (a > 0 && (t[r] = n[a - 1]), n[a] = r);
		}
	}
	for (a = n.length, o = n[a - 1]; a-- > 0;) n[a] = o, o = t[o];
	return n;
}
function ji(e) {
	let t = e.subTree.component;
	if (t) return t.asyncDep && !t.asyncResolved ? t : ji(t);
}
function Mi(e) {
	if (e) for (let t = 0; t < e.length; t++) e[t].flags |= 8;
}
function Ni(e) {
	if (e.placeholder) return e.placeholder;
	let t = e.component;
	return t ? Ni(t.subTree) : null;
}
var Pi = (e) => e.__isSuspense;
function Fi(e, t) {
	t && t.pendingBranch ? d(e) ? t.effects.push(...e) : t.effects.push(e) : vn(e);
}
var Ii = /* @__PURE__ */ Symbol.for("v-fgt"), Li = /* @__PURE__ */ Symbol.for("v-txt"), Ri = /* @__PURE__ */ Symbol.for("v-cmt"), zi = /* @__PURE__ */ Symbol.for("v-stc"), Bi = [], Vi = null;
function Hi(e = !1) {
	Bi.push(Vi = e ? null : []);
}
function Ui() {
	Bi.pop(), Vi = Bi[Bi.length - 1] || null;
}
var Wi = 1;
function Gi(e, t = !1) {
	Wi += e, e < 0 && Vi && t && (Vi.hasOnce = !0);
}
function Ki(e) {
	return e.dynamicChildren = Wi > 0 ? Vi || n : null, Ui(), Wi > 0 && Vi && Vi.push(e), e;
}
function qi(e, t, n, r, i, a) {
	return Ki($i(e, t, n, r, i, a, !0));
}
function Ji(e, t, n, r, i) {
	return Ki(ea(e, t, n, r, i, !0));
}
function Yi(e) {
	return e ? e.__v_isVNode === !0 : !1;
}
function Xi(e, t) {
	return e.type === t.type && e.key === t.key;
}
var Zi = ({ key: e }) => e ?? null, Qi = ({ ref: e, ref_key: t, ref_for: n }) => (typeof e == "number" && (e = "" + e), e == null ? null : g(e) || /* @__PURE__ */ Wt(e) || h(e) ? {
	i: Cn,
	r: e,
	k: t,
	f: !!n
} : e);
function $i(e, t = null, n = null, r = 0, i = null, a = e === Ii ? 0 : 1, o = !1, s = !1) {
	let c = {
		__v_isVNode: !0,
		__v_skip: !0,
		type: e,
		props: t,
		key: t && Zi(t),
		ref: t && Qi(t),
		scopeId: wn,
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
		shapeFlag: a,
		patchFlag: r,
		dynamicProps: i,
		dynamicChildren: null,
		appContext: null,
		ctx: Cn
	};
	return s ? (ca(c, n), a & 128 && e.normalize(c)) : n && (c.shapeFlag |= g(n) ? 8 : 16), Wi > 0 && !o && Vi && (c.patchFlag > 0 || a & 6) && c.patchFlag !== 32 && Vi.push(c), c;
}
var ea = ta;
function ta(e, t = null, n = null, r = 0, i = null, a = !1) {
	if ((!e || e === Sr) && (e = Ri), Yi(e)) {
		let r = ra(e, t, !0);
		return n && ca(r, n), Wi > 0 && !a && Vi && (r.shapeFlag & 6 ? Vi[Vi.indexOf(e)] = r : Vi.push(r)), r.patchFlag = -2, r;
	}
	if (Aa(e) && (e = e.__vccOpts), t) {
		t = na(t);
		let { class: e, style: n } = t;
		e && !g(e) && (t.class = me(e)), v(n) && (/* @__PURE__ */ Bt(n) && !d(n) && (n = s({}, n)), t.style = le(n));
	}
	let o = g(e) ? 1 : Pi(e) ? 128 : Rn(e) ? 64 : v(e) ? 4 : h(e) ? 2 : 0;
	return $i(e, t, n, r, i, o, a, !0);
}
function na(e) {
	return e ? /* @__PURE__ */ Bt(e) || si(e) ? s({}, e) : e : null;
}
function ra(e, t, n = !1, r = !1) {
	let { props: i, ref: a, patchFlag: o, children: s, transition: c } = e, l = t ? la(i || {}, t) : i, u = {
		__v_isVNode: !0,
		__v_skip: !0,
		type: e.type,
		props: l,
		key: l && Zi(l),
		ref: t && t.ref ? n && a ? d(a) ? a.concat(Qi(t)) : [a, Qi(t)] : Qi(t) : a,
		scopeId: e.scopeId,
		slotScopeIds: e.slotScopeIds,
		children: s,
		target: e.target,
		targetStart: e.targetStart,
		targetAnchor: e.targetAnchor,
		staticCount: e.staticCount,
		shapeFlag: e.shapeFlag,
		patchFlag: t && e.type !== Ii ? o === -1 ? 16 : o | 16 : o,
		dynamicProps: e.dynamicProps,
		dynamicChildren: e.dynamicChildren,
		appContext: e.appContext,
		dirs: e.dirs,
		transition: c,
		component: e.component,
		suspense: e.suspense,
		ssContent: e.ssContent && ra(e.ssContent),
		ssFallback: e.ssFallback && ra(e.ssFallback),
		placeholder: e.placeholder,
		el: e.el,
		anchor: e.anchor,
		ctx: e.ctx,
		ce: e.ce
	};
	return c && r && Zn(u, c.clone(u)), u;
}
function ia(e = " ", t = 0) {
	return ea(Li, null, e, t);
}
function aa(e = "", t = !1) {
	return t ? (Hi(), Ji(Ri, null, e)) : ea(Ri, null, e);
}
function oa(e) {
	return e == null || typeof e == "boolean" ? ea(Ri) : d(e) ? ea(Ii, null, e.slice()) : Yi(e) ? sa(e) : ea(Li, null, String(e));
}
function sa(e) {
	return e.el === null && e.patchFlag !== -1 || e.memo ? e : ra(e);
}
function ca(e, t) {
	let n = 0, { shapeFlag: r } = e;
	if (t == null) t = null;
	else if (d(t)) n = 16;
	else if (typeof t == "object") if (r & 65) {
		let n = t.default;
		n && (n._c && (n._d = !1), ca(e, n()), n._c && (n._d = !0));
		return;
	} else {
		n = 32;
		let r = t._;
		!r && !si(t) ? t._ctx = Cn : r === 3 && Cn && (Cn.slots._ === 1 ? t._ = 1 : (t._ = 2, e.patchFlag |= 1024));
	}
	else h(t) ? (t = {
		default: t,
		_ctx: Cn
	}, n = 32) : (t = String(t), r & 64 ? (n = 16, t = [ia(t)]) : n = 8);
	e.children = t, e.shapeFlag |= n;
}
function la(...e) {
	let t = {};
	for (let n = 0; n < e.length; n++) {
		let r = e[n];
		for (let e in r) if (e === "class") t.class !== r.class && (t.class = me([t.class, r.class]));
		else if (e === "style") t.style = le([t.style, r.style]);
		else if (a(e)) {
			let n = t[e], i = r[e];
			i && n !== i && !(d(n) && n.includes(i)) ? t[e] = n ? [].concat(n, i) : i : i == null && n == null && !o(e) && (t[e] = i);
		} else e !== "" && (t[e] = r[e]);
	}
	return t;
}
function ua(e, t, n, r = null) {
	rn(e, t, 7, [n, r]);
}
var da = Ur(), fa = 0;
function pa(e, n, r) {
	let i = e.type, a = (n ? n.appContext : e.appContext) || da, o = {
		uid: fa++,
		vnode: e,
		type: i,
		parent: n,
		appContext: a,
		root: null,
		next: null,
		subTree: null,
		effect: null,
		update: null,
		job: null,
		scope: new we(!0),
		render: null,
		proxy: null,
		exposed: null,
		exposeProxy: null,
		withProxy: null,
		provides: n ? n.provides : Object.create(a.provides),
		ids: n ? n.ids : [
			"",
			0,
			0
		],
		accessCache: null,
		renderCache: [],
		components: null,
		directives: null,
		propsOptions: pi(i, a),
		emitsOptions: Xr(i, a),
		emit: null,
		emitted: null,
		propsDefaults: t,
		inheritAttrs: i.inheritAttrs,
		ctx: t,
		data: t,
		props: t,
		attrs: t,
		slots: t,
		refs: t,
		setupState: t,
		setupContext: null,
		suspense: r,
		suspenseId: r ? r.pendingId : 0,
		asyncDep: null,
		asyncResolved: !1,
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
	return o.ctx = { _: o }, o.root = n ? n.root : o, o.emit = Jr.bind(null, o), e.ce && e.ce(o), o;
}
var I = null, ma = () => I || Cn, ha, ga;
{
	let e = ce(), t = (t, n) => {
		let r;
		return (r = e[t]) || (r = e[t] = []), r.push(n), (e) => {
			r.length > 1 ? r.forEach((t) => t(e)) : r[0](e);
		};
	};
	ha = t("__VUE_INSTANCE_SETTERS__", (e) => I = e), ga = t("__VUE_SSR_SETTERS__", (e) => ba = e);
}
var _a = (e) => {
	let t = I;
	return ha(e), e.scope.on(), () => {
		e.scope.off(), ha(t);
	};
}, va = () => {
	I && I.scope.off(), ha(null);
};
function ya(e) {
	return e.vnode.shapeFlag & 4;
}
var ba = !1;
function xa(e, t = !1, n = !1) {
	t && ga(t);
	let { props: r, children: i } = e.vnode, a = ya(e);
	ci(e, r, a, t), xi(e, i, n || t);
	let o = a ? Sa(e, t) : void 0;
	return t && ga(!1), o;
}
function Sa(e, t) {
	let n = e.type;
	e.accessCache = /* @__PURE__ */ Object.create(null), e.proxy = new Proxy(e.ctx, Dr);
	let { setup: r } = n;
	if (r) {
		He();
		let n = e.setupContext = r.length > 1 ? Oa(e) : null, i = _a(e), a = nn(r, e, 0, [e.props, n]), o = y(a);
		if (Ue(), i(), (o || e.sp) && !ir(e) && $n(e), o) {
			if (a.then(va, va), t) return a.then((n) => {
				Ca(e, n, t);
			}).catch((t) => {
				an(t, e, 0);
			});
			e.asyncDep = a;
		} else Ca(e, a, t);
	} else Ea(e, t);
}
function Ca(e, t, n) {
	h(t) ? e.type.__ssrInlineRender ? e.ssrRender = t : e.render = t : v(t) && (e.setupState = qt(t)), Ea(e, n);
}
var wa, Ta;
function Ea(e, t, n) {
	let i = e.type;
	if (!e.render) {
		if (!t && wa && !i.render) {
			let t = i.template || Pr(e).template;
			if (t) {
				let { isCustomElement: n, compilerOptions: r } = e.appContext.config, { delimiters: a, compilerOptions: o } = i;
				i.render = wa(t, s(s({
					isCustomElement: n,
					delimiters: a
				}, r), o));
			}
		}
		e.render = i.render || r, Ta && Ta(e);
	}
	{
		let t = _a(e);
		He();
		try {
			Ar(e);
		} finally {
			Ue(), t();
		}
	}
}
var Da = { get(e, t) {
	return N(e, "get", ""), e[t];
} };
function Oa(e) {
	return {
		attrs: new Proxy(e.attrs, Da),
		slots: e.slots,
		emit: e.emit,
		expose: (t) => {
			e.exposed = t || {};
		}
	};
}
function ka(e) {
	return e.exposed ? e.exposeProxy ||= new Proxy(qt(Vt(e.exposed)), {
		get(t, n) {
			if (n in t) return t[n];
			if (n in Tr) return Tr[n](e);
		},
		has(e, t) {
			return t in e || t in Tr;
		}
	}) : e.proxy;
}
function Aa(e) {
	return h(e) && "__vccOpts" in e;
}
var ja = (e, t) => /* @__PURE__ */ Yt(e, t, ba), Ma = "3.5.35", Na = void 0, Pa = typeof window < "u" && window.trustedTypes;
if (Pa) try {
	Na = /* @__PURE__ */ Pa.createPolicy("vue", { createHTML: (e) => e });
} catch {}
var Fa = Na ? (e) => Na.createHTML(e) : (e) => e, Ia = "http://www.w3.org/2000/svg", La = "http://www.w3.org/1998/Math/MathML", Ra = typeof document < "u" ? document : null, za = Ra && /* @__PURE__ */ Ra.createElement("template"), Ba = {
	insert: (e, t, n) => {
		t.insertBefore(e, n || null);
	},
	remove: (e) => {
		let t = e.parentNode;
		t && t.removeChild(e);
	},
	createElement: (e, t, n, r) => {
		let i = t === "svg" ? Ra.createElementNS(Ia, e) : t === "mathml" ? Ra.createElementNS(La, e) : n ? Ra.createElement(e, { is: n }) : Ra.createElement(e);
		return e === "select" && r && r.multiple != null && i.setAttribute("multiple", r.multiple), i;
	},
	createText: (e) => Ra.createTextNode(e),
	createComment: (e) => Ra.createComment(e),
	setText: (e, t) => {
		e.nodeValue = t;
	},
	setElementText: (e, t) => {
		e.textContent = t;
	},
	parentNode: (e) => e.parentNode,
	nextSibling: (e) => e.nextSibling,
	querySelector: (e) => Ra.querySelector(e),
	setScopeId(e, t) {
		e.setAttribute(t, "");
	},
	insertStaticContent(e, t, n, r, i, a) {
		let o = n ? n.previousSibling : t.lastChild;
		if (i && (i === a || i.nextSibling)) for (; t.insertBefore(i.cloneNode(!0), n), !(i === a || !(i = i.nextSibling)););
		else {
			za.innerHTML = Fa(r === "svg" ? `<svg>${e}</svg>` : r === "mathml" ? `<math>${e}</math>` : e);
			let i = za.content;
			if (r === "svg" || r === "mathml") {
				let e = i.firstChild;
				for (; e.firstChild;) i.appendChild(e.firstChild);
				i.removeChild(e);
			}
			t.insertBefore(i, n);
		}
		return [o ? o.nextSibling : t.firstChild, n ? n.previousSibling : t.lastChild];
	}
}, Va = /* @__PURE__ */ Symbol("_vtc");
function Ha(e, t, n) {
	let r = e[Va];
	r && (t = (t ? [t, ...r] : [...r]).join(" ")), t == null ? e.removeAttribute("class") : n ? e.setAttribute("class", t) : e.className = t;
}
var Ua = /* @__PURE__ */ Symbol("_vod"), Wa = /* @__PURE__ */ Symbol("_vsh"), Ga = /* @__PURE__ */ Symbol(""), Ka = /(?:^|;)\s*display\s*:/;
function qa(e, t, n) {
	let r = e.style, i = g(n), a = !1;
	if (n && !i) {
		if (t) if (g(t)) for (let e of t.split(";")) {
			let t = e.slice(0, e.indexOf(":")).trim();
			n[t] ?? Ya(r, t, "");
		}
		else for (let e in t) n[e] ?? Ya(r, e, "");
		for (let i in n) {
			i === "display" && (a = !0);
			let o = n[i];
			o == null ? Ya(r, i, "") : $a(e, i, !g(t) && t ? t[i] : void 0, o) || Ya(r, i, o);
		}
	} else if (i) {
		if (t !== n) {
			let e = r[Ga];
			e && (n += ";" + e), r.cssText = n, a = Ka.test(n);
		}
	} else t && e.removeAttribute("style");
	Ua in e && (e[Ua] = a ? r.display : "", e[Wa] && (r.display = "none"));
}
var Ja = /\s*!important$/;
function Ya(e, t, n) {
	if (d(n)) n.forEach((n) => Ya(e, t, n));
	else if (n ??= "", t.startsWith("--")) e.setProperty(t, n);
	else {
		let r = Qa(e, t);
		Ja.test(n) ? e.setProperty(k(r), n.replace(Ja, ""), "important") : e[r] = n;
	}
}
var Xa = [
	"Webkit",
	"Moz",
	"ms"
], Za = {};
function Qa(e, t) {
	let n = Za[t];
	if (n) return n;
	let r = O(t);
	if (r !== "filter" && r in e) return Za[t] = r;
	r = te(r);
	for (let n = 0; n < Xa.length; n++) {
		let i = Xa[n] + r;
		if (i in e) return Za[t] = i;
	}
	return t;
}
function $a(e, t, n, r) {
	return e.tagName === "TEXTAREA" && (t === "width" || t === "height") && g(r) && n === r;
}
var eo = "http://www.w3.org/1999/xlink";
function to(e, t, n, r, i, a = ge(t)) {
	r && t.startsWith("xlink:") ? n == null ? e.removeAttributeNS(eo, t.slice(6, t.length)) : e.setAttributeNS(eo, t, n) : n == null || a && !_e(n) ? e.removeAttribute(t) : e.setAttribute(t, a ? "" : _(n) ? String(n) : n);
}
function no(e, t, n, r, i) {
	if (t === "innerHTML" || t === "textContent") {
		n != null && (e[t] = t === "innerHTML" ? Fa(n) : n);
		return;
	}
	let a = e.tagName;
	if (t === "value" && a !== "PROGRESS" && !a.includes("-")) {
		let r = a === "OPTION" ? e.getAttribute("value") || "" : e.value, i = n == null ? e.type === "checkbox" ? "on" : "" : String(n);
		(r !== i || !("_value" in e)) && (e.value = i), n ?? e.removeAttribute(t), e._value = n;
		return;
	}
	let o = !1;
	if (n === "" || n == null) {
		let r = typeof e[t];
		r === "boolean" ? n = _e(n) : n == null && r === "string" ? (n = "", o = !0) : r === "number" && (n = 0, o = !0);
	}
	try {
		e[t] = n;
	} catch {}
	o && e.removeAttribute(i || t);
}
function ro(e, t, n, r) {
	e.addEventListener(t, n, r);
}
function io(e, t, n, r) {
	e.removeEventListener(t, n, r);
}
var ao = /* @__PURE__ */ Symbol("_vei");
function oo(e, t, n, r, i = null) {
	let a = e[ao] || (e[ao] = {}), o = a[t];
	if (r && o) o.value = r;
	else {
		let [n, s] = co(t);
		r ? ro(e, n, a[t] = po(r, i), s) : o && (io(e, n, o, s), a[t] = void 0);
	}
}
var so = /(?:Once|Passive|Capture)$/;
function co(e) {
	let t;
	if (so.test(e)) {
		t = {};
		let n;
		for (; n = e.match(so);) e = e.slice(0, e.length - n[0].length), t[n[0].toLowerCase()] = !0;
	}
	return [e[2] === ":" ? e.slice(3) : k(e.slice(2)), t];
}
var lo = 0, uo = /* @__PURE__ */ Promise.resolve(), fo = () => lo ||= (uo.then(() => lo = 0), Date.now());
function po(e, t) {
	let n = (e) => {
		if (!e._vts) e._vts = Date.now();
		else if (e._vts <= n.attached) return;
		let r = n.value;
		if (d(r)) {
			let n = e.stopImmediatePropagation;
			e.stopImmediatePropagation = () => {
				n.call(e), e._stopped = !0;
			};
			let i = r.slice(), a = [e];
			for (let n = 0; n < i.length && !e._stopped; n++) {
				let e = i[n];
				e && rn(e, t, 5, a);
			}
		} else rn(r, t, 5, [e]);
	};
	return n.value = e, n.attached = fo(), n;
}
var mo = (e) => e.charCodeAt(0) === 111 && e.charCodeAt(1) === 110 && e.charCodeAt(2) > 96 && e.charCodeAt(2) < 123, ho = (e, t, n, r, i, s) => {
	let c = i === "svg";
	t === "class" ? Ha(e, r, c) : t === "style" ? qa(e, n, r) : a(t) ? o(t) || oo(e, t, n, r, s) : (t[0] === "." ? (t = t.slice(1), !0) : t[0] === "^" ? (t = t.slice(1), !1) : go(e, t, r, c)) ? (no(e, t, r), !e.tagName.includes("-") && (t === "value" || t === "checked" || t === "selected") && to(e, t, r, c, s, t !== "value")) : e._isVueCE && (_o(e, t) || e._def.__asyncLoader && (/[A-Z]/.test(t) || !g(r))) ? no(e, O(t), r, s, t) : (t === "true-value" ? e._trueValue = r : t === "false-value" && (e._falseValue = r), to(e, t, r, c));
};
function go(e, t, n, r) {
	if (r) return !!(t === "innerHTML" || t === "textContent" || t in e && mo(t) && h(n));
	if (t === "spellcheck" || t === "draggable" || t === "translate" || t === "autocorrect" || t === "sandbox" && e.tagName === "IFRAME" || t === "form" || t === "list" && e.tagName === "INPUT" || t === "type" && e.tagName === "TEXTAREA") return !1;
	if (t === "width" || t === "height") {
		let t = e.tagName;
		if (t === "IMG" || t === "VIDEO" || t === "CANVAS" || t === "SOURCE") return !1;
	}
	return mo(t) && g(n) ? !1 : t in e;
}
function _o(e, t) {
	let n = e._def.props;
	if (!n) return !1;
	let r = O(t);
	return Array.isArray(n) ? n.some((e) => O(e) === r) : Object.keys(n).some((e) => O(e) === r);
}
var vo = {};
// @__NO_SIDE_EFFECTS__
function yo(e, t, n) {
	let r = /* @__PURE__ */ Qn(e, t);
	C(r) && (r = s({}, r, t));
	class i extends xo {
		constructor(e) {
			super(r, e, n);
		}
	}
	return i.def = r, i;
}
var bo = typeof HTMLElement < "u" ? HTMLElement : class {}, xo = class e extends bo {
	constructor(e, t = {}, n = Eo) {
		super(), this._def = e, this._props = t, this._createApp = n, this._isVueCE = !0, this._instance = null, this._app = null, this._nonce = this._def.nonce, this._connected = !1, this._resolved = !1, this._patching = !1, this._dirty = !1, this._numberProps = null, this._styleChildren = /* @__PURE__ */ new WeakSet(), this._styleAnchors = /* @__PURE__ */ new WeakMap(), this._ob = null, this.shadowRoot && n !== Eo ? this._root = this.shadowRoot : e.shadowRoot === !1 ? this._root = this : (this.attachShadow(s({}, e.shadowRootOptions, { mode: "open" })), this._root = this.shadowRoot);
	}
	connectedCallback() {
		if (!this.isConnected) return;
		!this.shadowRoot && !this._resolved && this._parseSlots(), this._connected = !0;
		let t = this;
		for (; t &&= t.assignedSlot || t.parentNode || t.host;) if (t instanceof e) {
			this._parent = t;
			break;
		}
		this._instance || (this._resolved ? this._mount(this._def) : t && t._pendingResolve ? this._pendingResolve = t._pendingResolve.then(() => {
			this._pendingResolve = void 0, this._resolveDef();
		}) : this._resolveDef());
	}
	_setParent(e = this._parent) {
		e && (this._instance.parent = e._instance, this._inheritParentContext(e));
	}
	_inheritParentContext(e = this._parent) {
		e && this._app && Object.setPrototypeOf(this._app._context.provides, e._instance.provides);
	}
	disconnectedCallback() {
		this._connected = !1, mn(() => {
			this._connected || (this._ob &&= (this._ob.disconnect(), null), this._app && this._app.unmount(), this._instance && (this._instance.ce = void 0), this._app = this._instance = null, this._teleportTargets &&= (this._teleportTargets.clear(), void 0));
		});
	}
	_processMutations(e) {
		for (let t of e) this._setAttr(t.attributeName);
	}
	_resolveDef() {
		if (this._pendingResolve) return;
		for (let e = 0; e < this.attributes.length; e++) this._setAttr(this.attributes[e].name);
		this._ob = new MutationObserver(this._processMutations.bind(this)), this._ob.observe(this, { attributes: !0 });
		let e = (e, t = !1) => {
			this._resolved = !0, this._pendingResolve = void 0;
			let { props: n, styles: r } = e, i;
			if (n && !d(n)) for (let e in n) {
				let t = n[e];
				(t === Number || t && t.type === Number) && (e in this._props && (this._props[e] = oe(this._props[e])), (i ||= /* @__PURE__ */ Object.create(null))[O(e)] = !0);
			}
			this._numberProps = i, this._resolveProps(e), this.shadowRoot && this._applyStyles(r), this._mount(e);
		}, t = this._def.__asyncLoader;
		t ? this._pendingResolve = t().then((t) => {
			t.configureApp = this._def.configureApp, e(this._def = t, !0);
		}) : e(this._def);
	}
	_mount(e) {
		this._app = this._createApp(e), this._inheritParentContext(), e.configureApp && e.configureApp(this._app), this._app._ceVNode = this._createVNode(), this._app.mount(this._root);
		let t = this._instance && this._instance.exposed;
		if (t) for (let e in t) u(this, e) || Object.defineProperty(this, e, { get: () => Gt(t[e]) });
	}
	_resolveProps(e) {
		let { props: t } = e, n = d(t) ? t : Object.keys(t || {});
		for (let e of Object.keys(this)) e[0] !== "_" && n.includes(e) && this._setProp(e, this[e]);
		for (let e of n.map(O)) Object.defineProperty(this, e, {
			get() {
				return this._getProp(e);
			},
			set(t) {
				this._setProp(e, t, !0, !this._patching);
			}
		});
	}
	_setAttr(e) {
		if (e.startsWith("data-v-")) return;
		let t = this.hasAttribute(e), n = t ? this.getAttribute(e) : vo, r = O(e);
		t && this._numberProps && this._numberProps[r] && (n = oe(n)), this._setProp(r, n, !1, !0);
	}
	_getProp(e) {
		return this._props[e];
	}
	_setProp(e, t, n = !0, r = !1) {
		if (t !== this._props[e] && (this._dirty = !0, t === vo ? delete this._props[e] : (this._props[e] = t, e === "key" && this._app && (this._app._ceVNode.key = t)), r && this._instance && this._update(), n)) {
			let n = this._ob;
			n && (this._processMutations(n.takeRecords()), n.disconnect()), t === !0 ? this.setAttribute(k(e), "") : typeof t == "string" || typeof t == "number" ? this.setAttribute(k(e), t + "") : t || this.removeAttribute(k(e)), n && n.observe(this, { attributes: !0 });
		}
	}
	_update() {
		let e = this._createVNode();
		this._app && (e.appContext = this._app._context), To(e, this._root);
	}
	_createVNode() {
		let e = {};
		this.shadowRoot || (e.onVnodeMounted = e.onVnodeUpdated = this._renderSlots.bind(this));
		let t = ea(this._def, s(e, this._props));
		return this._instance || (t.ce = (e) => {
			this._instance = e, e.ce = this, e.isCE = !0;
			let t = (e, t) => {
				this.dispatchEvent(new CustomEvent(e, C(t[0]) ? s({ detail: t }, t[0]) : { detail: t }));
			};
			e.emit = (e, ...n) => {
				t(e, n), k(e) !== e && t(k(e), n);
			}, this._setParent();
		}), t;
	}
	_applyStyles(e, t, n) {
		if (!e) return;
		if (t) {
			if (t === this._def || this._styleChildren.has(t)) return;
			this._styleChildren.add(t);
		}
		let r = this._nonce, i = this.shadowRoot, a = n ? this._getStyleAnchor(n) || this._getStyleAnchor(this._def) : this._getRootStyleInsertionAnchor(i), o = null;
		for (let s = e.length - 1; s >= 0; s--) {
			let c = document.createElement("style");
			r && c.setAttribute("nonce", r), c.textContent = e[s], i.insertBefore(c, o || a), o = c, s === 0 && (n || this._styleAnchors.set(this._def, c), t && this._styleAnchors.set(t, c));
		}
	}
	_getStyleAnchor(e) {
		if (!e) return null;
		let t = this._styleAnchors.get(e);
		return t && t.parentNode === this.shadowRoot ? t : (t && this._styleAnchors.delete(e), null);
	}
	_getRootStyleInsertionAnchor(e) {
		for (let t = 0; t < e.childNodes.length; t++) {
			let n = e.childNodes[t];
			if (!(n instanceof HTMLStyleElement)) return n;
		}
		return null;
	}
	_parseSlots() {
		let e = this._slots = {}, t;
		for (; t = this.firstChild;) {
			let n = t.nodeType === 1 && t.getAttribute("slot") || "default";
			(e[n] || (e[n] = [])).push(t), this.removeChild(t);
		}
	}
	_renderSlots() {
		let e = this._getSlots(), t = this._instance.type.__scopeId;
		for (let n = 0; n < e.length; n++) {
			let r = e[n], i = r.getAttribute("name") || "default", a = this._slots[i], o = r.parentNode;
			if (a) for (let e of a) {
				if (t && e.nodeType === 1) {
					let n = t + "-s", r = document.createTreeWalker(e, 1);
					e.setAttribute(n, "");
					let i;
					for (; i = r.nextNode();) i.setAttribute(n, "");
				}
				o.insertBefore(e, r);
			}
			else for (; r.firstChild;) o.insertBefore(r.firstChild, r);
			o.removeChild(r);
		}
	}
	_getSlots() {
		let e = [this];
		this._teleportTargets && e.push(...this._teleportTargets);
		let t = /* @__PURE__ */ new Set();
		for (let n of e) {
			let e = n.querySelectorAll("slot");
			for (let n = 0; n < e.length; n++) t.add(e[n]);
		}
		return Array.from(t);
	}
	_injectChildStyle(e, t) {
		this._applyStyles(e.styles, e, t);
	}
	_beginPatch() {
		this._patching = !0, this._dirty = !1;
	}
	_endPatch() {
		this._patching = !1, this._dirty && this._instance && this._update();
	}
	_hasShadowRoot() {
		return this._def.shadowRoot !== !1;
	}
	_removeChildStyle(e) {}
}, So = /* @__PURE__ */ s({ patchProp: ho }, Ba), Co;
function wo() {
	return Co ||= wi(So);
}
var To = ((...e) => {
	wo().render(...e);
}), Eo = ((...e) => {
	let t = wo().createApp(...e), { mount: n } = t;
	return t.mount = (e) => {
		let r = Oo(e);
		if (!r) return;
		let i = t._component;
		!h(i) && !i.render && !i.template && (i.template = r.innerHTML), r.nodeType === 1 && (r.textContent = "");
		let a = n(r, !1, Do(r));
		return r instanceof Element && (r.removeAttribute("v-cloak"), r.setAttribute("data-v-app", "")), a;
	}, t;
});
function Do(e) {
	if (e instanceof SVGElement) return "svg";
	if (typeof MathMLElement == "function" && e instanceof MathMLElement) return "mathml";
}
function Oo(e) {
	return g(e) ? document.querySelector(e) : e;
}
//#endregion
//#region node_modules/@kurkle/color/dist/color.esm.js
function ko(e) {
	return e + .5 | 0;
}
var Ao = (e, t, n) => Math.max(Math.min(e, n), t);
function jo(e) {
	return Ao(ko(e * 2.55), 0, 255);
}
function Mo(e) {
	return Ao(ko(e * 255), 0, 255);
}
function No(e) {
	return Ao(ko(e / 2.55) / 100, 0, 1);
}
function Po(e) {
	return Ao(ko(e * 100), 0, 100);
}
var Fo = {
	0: 0,
	1: 1,
	2: 2,
	3: 3,
	4: 4,
	5: 5,
	6: 6,
	7: 7,
	8: 8,
	9: 9,
	A: 10,
	B: 11,
	C: 12,
	D: 13,
	E: 14,
	F: 15,
	a: 10,
	b: 11,
	c: 12,
	d: 13,
	e: 14,
	f: 15
}, Io = [..."0123456789ABCDEF"], Lo = (e) => Io[e & 15], Ro = (e) => Io[(e & 240) >> 4] + Io[e & 15], zo = (e) => (e & 240) >> 4 == (e & 15), Bo = (e) => zo(e.r) && zo(e.g) && zo(e.b) && zo(e.a);
function Vo(e) {
	var t = e.length, n;
	return e[0] === "#" && (t === 4 || t === 5 ? n = {
		r: 255 & Fo[e[1]] * 17,
		g: 255 & Fo[e[2]] * 17,
		b: 255 & Fo[e[3]] * 17,
		a: t === 5 ? Fo[e[4]] * 17 : 255
	} : (t === 7 || t === 9) && (n = {
		r: Fo[e[1]] << 4 | Fo[e[2]],
		g: Fo[e[3]] << 4 | Fo[e[4]],
		b: Fo[e[5]] << 4 | Fo[e[6]],
		a: t === 9 ? Fo[e[7]] << 4 | Fo[e[8]] : 255
	})), n;
}
var Ho = (e, t) => e < 255 ? t(e) : "";
function Uo(e) {
	var t = Bo(e) ? Lo : Ro;
	return e ? "#" + t(e.r) + t(e.g) + t(e.b) + Ho(e.a, t) : void 0;
}
var Wo = /^(hsla?|hwb|hsv)\(\s*([-+.e\d]+)(?:deg)?[\s,]+([-+.e\d]+)%[\s,]+([-+.e\d]+)%(?:[\s,]+([-+.e\d]+)(%)?)?\s*\)$/;
function Go(e, t, n) {
	let r = t * Math.min(n, 1 - n), i = (t, i = (t + e / 30) % 12) => n - r * Math.max(Math.min(i - 3, 9 - i, 1), -1);
	return [
		i(0),
		i(8),
		i(4)
	];
}
function Ko(e, t, n) {
	let r = (r, i = (r + e / 60) % 6) => n - n * t * Math.max(Math.min(i, 4 - i, 1), 0);
	return [
		r(5),
		r(3),
		r(1)
	];
}
function qo(e, t, n) {
	let r = Go(e, 1, .5), i;
	for (t + n > 1 && (i = 1 / (t + n), t *= i, n *= i), i = 0; i < 3; i++) r[i] *= 1 - t - n, r[i] += t;
	return r;
}
function Jo(e, t, n, r, i) {
	return e === i ? (t - n) / r + (t < n ? 6 : 0) : t === i ? (n - e) / r + 2 : (e - t) / r + 4;
}
function Yo(e) {
	let t = e.r / 255, n = e.g / 255, r = e.b / 255, i = Math.max(t, n, r), a = Math.min(t, n, r), o = (i + a) / 2, s, c, l;
	return i !== a && (l = i - a, c = o > .5 ? l / (2 - i - a) : l / (i + a), s = Jo(t, n, r, l, i), s = s * 60 + .5), [
		s | 0,
		c || 0,
		o
	];
}
function Xo(e, t, n, r) {
	return (Array.isArray(t) ? e(t[0], t[1], t[2]) : e(t, n, r)).map(Mo);
}
function Zo(e, t, n) {
	return Xo(Go, e, t, n);
}
function Qo(e, t, n) {
	return Xo(qo, e, t, n);
}
function $o(e, t, n) {
	return Xo(Ko, e, t, n);
}
function es(e) {
	return (e % 360 + 360) % 360;
}
function ts(e) {
	let t = Wo.exec(e), n = 255, r;
	if (!t) return;
	t[5] !== r && (n = t[6] ? jo(+t[5]) : Mo(+t[5]));
	let i = es(+t[2]), a = t[3] / 100, o = t[4] / 100;
	return r = t[1] === "hwb" ? Qo(i, a, o) : t[1] === "hsv" ? $o(i, a, o) : Zo(i, a, o), {
		r: r[0],
		g: r[1],
		b: r[2],
		a: n
	};
}
function ns(e, t) {
	var n = Yo(e);
	n[0] = es(n[0] + t), n = Zo(n), e.r = n[0], e.g = n[1], e.b = n[2];
}
function rs(e) {
	if (!e) return;
	let t = Yo(e), n = t[0], r = Po(t[1]), i = Po(t[2]);
	return e.a < 255 ? `hsla(${n}, ${r}%, ${i}%, ${No(e.a)})` : `hsl(${n}, ${r}%, ${i}%)`;
}
var is = {
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
}, as = {
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
function os() {
	let e = {}, t = Object.keys(as), n = Object.keys(is), r, i, a, o, s;
	for (r = 0; r < t.length; r++) {
		for (o = s = t[r], i = 0; i < n.length; i++) a = n[i], s = s.replace(a, is[a]);
		a = parseInt(as[o], 16), e[s] = [
			a >> 16 & 255,
			a >> 8 & 255,
			a & 255
		];
	}
	return e;
}
var ss;
function cs(e) {
	ss || (ss = os(), ss.transparent = [
		0,
		0,
		0,
		0
	]);
	let t = ss[e.toLowerCase()];
	return t && {
		r: t[0],
		g: t[1],
		b: t[2],
		a: t.length === 4 ? t[3] : 255
	};
}
var ls = /^rgba?\(\s*([-+.\d]+)(%)?[\s,]+([-+.e\d]+)(%)?[\s,]+([-+.e\d]+)(%)?(?:[\s,/]+([-+.e\d]+)(%)?)?\s*\)$/;
function us(e) {
	let t = ls.exec(e), n = 255, r, i, a;
	if (t) {
		if (t[7] !== r) {
			let e = +t[7];
			n = t[8] ? jo(e) : Ao(e * 255, 0, 255);
		}
		return r = +t[1], i = +t[3], a = +t[5], r = 255 & (t[2] ? jo(r) : Ao(r, 0, 255)), i = 255 & (t[4] ? jo(i) : Ao(i, 0, 255)), a = 255 & (t[6] ? jo(a) : Ao(a, 0, 255)), {
			r,
			g: i,
			b: a,
			a: n
		};
	}
}
function ds(e) {
	return e && (e.a < 255 ? `rgba(${e.r}, ${e.g}, ${e.b}, ${No(e.a)})` : `rgb(${e.r}, ${e.g}, ${e.b})`);
}
var fs = (e) => e <= .0031308 ? e * 12.92 : e ** (1 / 2.4) * 1.055 - .055, ps = (e) => e <= .04045 ? e / 12.92 : ((e + .055) / 1.055) ** 2.4;
function ms(e, t, n) {
	let r = ps(No(e.r)), i = ps(No(e.g)), a = ps(No(e.b));
	return {
		r: Mo(fs(r + n * (ps(No(t.r)) - r))),
		g: Mo(fs(i + n * (ps(No(t.g)) - i))),
		b: Mo(fs(a + n * (ps(No(t.b)) - a))),
		a: e.a + n * (t.a - e.a)
	};
}
function hs(e, t, n) {
	if (e) {
		let r = Yo(e);
		r[t] = Math.max(0, Math.min(r[t] + r[t] * n, t === 0 ? 360 : 1)), r = Zo(r), e.r = r[0], e.g = r[1], e.b = r[2];
	}
}
function gs(e, t) {
	return e && Object.assign(t || {}, e);
}
function _s(e) {
	var t = {
		r: 0,
		g: 0,
		b: 0,
		a: 255
	};
	return Array.isArray(e) ? e.length >= 3 && (t = {
		r: e[0],
		g: e[1],
		b: e[2],
		a: 255
	}, e.length > 3 && (t.a = Mo(e[3]))) : (t = gs(e, {
		r: 0,
		g: 0,
		b: 0,
		a: 1
	}), t.a = Mo(t.a)), t;
}
function vs(e) {
	return e.charAt(0) === "r" ? us(e) : ts(e);
}
var ys = class e {
	constructor(t) {
		if (t instanceof e) return t;
		let n = typeof t, r;
		n === "object" ? r = _s(t) : n === "string" && (r = Vo(t) || cs(t) || vs(t)), this._rgb = r, this._valid = !!r;
	}
	get valid() {
		return this._valid;
	}
	get rgb() {
		var e = gs(this._rgb);
		return e && (e.a = No(e.a)), e;
	}
	set rgb(e) {
		this._rgb = _s(e);
	}
	rgbString() {
		return this._valid ? ds(this._rgb) : void 0;
	}
	hexString() {
		return this._valid ? Uo(this._rgb) : void 0;
	}
	hslString() {
		return this._valid ? rs(this._rgb) : void 0;
	}
	mix(e, t) {
		if (e) {
			let n = this.rgb, r = e.rgb, i, a = t === i ? .5 : t, o = 2 * a - 1, s = n.a - r.a, c = ((o * s === -1 ? o : (o + s) / (1 + o * s)) + 1) / 2;
			i = 1 - c, n.r = 255 & c * n.r + i * r.r + .5, n.g = 255 & c * n.g + i * r.g + .5, n.b = 255 & c * n.b + i * r.b + .5, n.a = a * n.a + (1 - a) * r.a, this.rgb = n;
		}
		return this;
	}
	interpolate(e, t) {
		return e && (this._rgb = ms(this._rgb, e._rgb, t)), this;
	}
	clone() {
		return new e(this.rgb);
	}
	alpha(e) {
		return this._rgb.a = Mo(e), this;
	}
	clearer(e) {
		let t = this._rgb;
		return t.a *= 1 - e, this;
	}
	greyscale() {
		let e = this._rgb;
		return e.r = e.g = e.b = ko(e.r * .3 + e.g * .59 + e.b * .11), this;
	}
	opaquer(e) {
		let t = this._rgb;
		return t.a *= 1 + e, this;
	}
	negate() {
		let e = this._rgb;
		return e.r = 255 - e.r, e.g = 255 - e.g, e.b = 255 - e.b, this;
	}
	lighten(e) {
		return hs(this._rgb, 2, e), this;
	}
	darken(e) {
		return hs(this._rgb, 2, -e), this;
	}
	saturate(e) {
		return hs(this._rgb, 1, e), this;
	}
	desaturate(e) {
		return hs(this._rgb, 1, -e), this;
	}
	rotate(e) {
		return ns(this._rgb, e), this;
	}
};
//#endregion
//#region node_modules/chart.js/dist/chunks/helpers.dataset.js
function bs() {}
var xs = (() => {
	let e = 0;
	return () => e++;
})();
function L(e) {
	return e == null;
}
function R(e) {
	if (Array.isArray && Array.isArray(e)) return !0;
	let t = Object.prototype.toString.call(e);
	return t.slice(0, 7) === "[object" && t.slice(-6) === "Array]";
}
function z(e) {
	return e !== null && Object.prototype.toString.call(e) === "[object Object]";
}
function B(e) {
	return (typeof e == "number" || e instanceof Number) && isFinite(+e);
}
function Ss(e, t) {
	return B(e) ? e : t;
}
function V(e, t) {
	return e === void 0 ? t : e;
}
var Cs = (e, t) => typeof e == "string" && e.endsWith("%") ? parseFloat(e) / 100 * t : +e;
function H(e, t, n) {
	if (e && typeof e.call == "function") return e.apply(n, t);
}
function U(e, t, n, r) {
	let i, a, o;
	if (R(e)) if (a = e.length, r) for (i = a - 1; i >= 0; i--) t.call(n, e[i], i);
	else for (i = 0; i < a; i++) t.call(n, e[i], i);
	else if (z(e)) for (o = Object.keys(e), a = o.length, i = 0; i < a; i++) t.call(n, e[o[i]], o[i]);
}
function ws(e, t) {
	let n, r, i, a;
	if (!e || !t || e.length !== t.length) return !1;
	for (n = 0, r = e.length; n < r; ++n) if (i = e[n], a = t[n], i.datasetIndex !== a.datasetIndex || i.index !== a.index) return !1;
	return !0;
}
function Ts(e) {
	if (R(e)) return e.map(Ts);
	if (z(e)) {
		let t = Object.create(null), n = Object.keys(e), r = n.length, i = 0;
		for (; i < r; ++i) t[n[i]] = Ts(e[n[i]]);
		return t;
	}
	return e;
}
function Es(e) {
	return [
		"__proto__",
		"prototype",
		"constructor"
	].indexOf(e) === -1;
}
function Ds(e, t, n, r) {
	if (!Es(e)) return;
	let i = t[e], a = n[e];
	z(i) && z(a) ? Os(i, a, r) : t[e] = Ts(a);
}
function Os(e, t, n) {
	let r = R(t) ? t : [t], i = r.length;
	if (!z(e)) return e;
	n ||= {};
	let a = n.merger || Ds, o;
	for (let t = 0; t < i; ++t) {
		if (o = r[t], !z(o)) continue;
		let i = Object.keys(o);
		for (let t = 0, r = i.length; t < r; ++t) a(i[t], e, o, n);
	}
	return e;
}
function ks(e, t) {
	return Os(e, t, { merger: As });
}
function As(e, t, n) {
	if (!Es(e)) return;
	let r = t[e], i = n[e];
	z(r) && z(i) ? ks(r, i) : Object.prototype.hasOwnProperty.call(t, e) || (t[e] = Ts(i));
}
var js = {
	"": (e) => e,
	x: (e) => e.x,
	y: (e) => e.y
};
function Ms(e) {
	let t = e.split("."), n = [], r = "";
	for (let e of t) r += e, r.endsWith("\\") ? r = r.slice(0, -1) + "." : (n.push(r), r = "");
	return n;
}
function Ns(e) {
	let t = Ms(e);
	return (e) => {
		for (let n of t) {
			if (n === "") break;
			e &&= e[n];
		}
		return e;
	};
}
function Ps(e, t) {
	return (js[t] || (js[t] = Ns(t)))(e);
}
function Fs(e) {
	return e.charAt(0).toUpperCase() + e.slice(1);
}
var Is = (e) => e !== void 0, Ls = (e) => typeof e == "function", Rs = (e, t) => {
	if (e.size !== t.size) return !1;
	for (let n of e) if (!t.has(n)) return !1;
	return !0;
};
function zs(e) {
	return e.type === "mouseup" || e.type === "click" || e.type === "contextmenu";
}
var W = Math.PI, Bs = 2 * W, Vs = Bs + W, Hs = Infinity, Us = W / 180, Ws = W / 2, Gs = W / 4, Ks = W * 2 / 3, qs = Math.log10, Js = Math.sign;
function Ys(e, t, n) {
	return Math.abs(e - t) < n;
}
function Xs(e) {
	let t = Math.round(e);
	e = Ys(e, t, e / 1e3) ? t : e;
	let n = 10 ** Math.floor(qs(e)), r = e / n;
	return (r <= 1 ? 1 : r <= 2 ? 2 : r <= 5 ? 5 : 10) * n;
}
function Zs(e) {
	let t = [], n = Math.sqrt(e), r;
	for (r = 1; r < n; r++) e % r === 0 && (t.push(r), t.push(e / r));
	return n === (n | 0) && t.push(n), t.sort((e, t) => e - t).pop(), t;
}
function Qs(e) {
	return typeof e == "symbol" || typeof e == "object" && !!e && !(Symbol.toPrimitive in e || "toString" in e || "valueOf" in e);
}
function $s(e) {
	return !Qs(e) && !isNaN(parseFloat(e)) && isFinite(e);
}
function ec(e, t) {
	let n = Math.round(e);
	return n - t <= e && n + t >= e;
}
function tc(e, t, n) {
	let r, i, a;
	for (r = 0, i = e.length; r < i; r++) a = e[r][n], isNaN(a) || (t.min = Math.min(t.min, a), t.max = Math.max(t.max, a));
}
function nc(e) {
	return W / 180 * e;
}
function rc(e) {
	return 180 / W * e;
}
function ic(e) {
	if (!B(e)) return;
	let t = 1, n = 0;
	for (; Math.round(e * t) / t !== e;) t *= 10, n++;
	return n;
}
function ac(e, t) {
	let n = t.x - e.x, r = t.y - e.y, i = Math.sqrt(n * n + r * r), a = Math.atan2(r, n);
	return a < -.5 * W && (a += Bs), {
		angle: a,
		distance: i
	};
}
function oc(e, t) {
	return Math.sqrt((t.x - e.x) ** 2 + (t.y - e.y) ** 2);
}
function sc(e, t) {
	return (e - t + Vs) % Bs - W;
}
function cc(e) {
	return (e % Bs + Bs) % Bs;
}
function lc(e, t, n, r) {
	let i = cc(e), a = cc(t), o = cc(n), s = cc(a - i), c = cc(o - i), l = cc(i - a), u = cc(i - o);
	return i === a || i === o || r && a === o || s > c && l < u;
}
function uc(e, t, n) {
	return Math.max(t, Math.min(n, e));
}
function dc(e) {
	return uc(e, -32768, 32767);
}
function fc(e, t, n, r = 1e-6) {
	return e >= Math.min(t, n) - r && e <= Math.max(t, n) + r;
}
function pc(e, t, n) {
	n ||= ((n) => e[n] < t);
	let r = e.length - 1, i = 0, a;
	for (; r - i > 1;) a = i + r >> 1, n(a) ? i = a : r = a;
	return {
		lo: i,
		hi: r
	};
}
var mc = (e, t, n, r) => pc(e, n, r ? (r) => {
	let i = e[r][t];
	return i < n || i === n && e[r + 1][t] === n;
} : (r) => e[r][t] < n), hc = (e, t, n) => pc(e, n, (r) => e[r][t] >= n);
function gc(e, t, n) {
	let r = 0, i = e.length;
	for (; r < i && e[r] < t;) r++;
	for (; i > r && e[i - 1] > n;) i--;
	return r > 0 || i < e.length ? e.slice(r, i) : e;
}
var _c = [
	"push",
	"pop",
	"shift",
	"splice",
	"unshift"
];
function vc(e, t) {
	if (e._chartjs) {
		e._chartjs.listeners.push(t);
		return;
	}
	Object.defineProperty(e, "_chartjs", {
		configurable: !0,
		enumerable: !1,
		value: { listeners: [t] }
	}), _c.forEach((t) => {
		let n = "_onData" + Fs(t), r = e[t];
		Object.defineProperty(e, t, {
			configurable: !0,
			enumerable: !1,
			value(...t) {
				let i = r.apply(this, t);
				return e._chartjs.listeners.forEach((e) => {
					typeof e[n] == "function" && e[n](...t);
				}), i;
			}
		});
	});
}
function yc(e, t) {
	let n = e._chartjs;
	if (!n) return;
	let r = n.listeners, i = r.indexOf(t);
	i !== -1 && r.splice(i, 1), !(r.length > 0) && (_c.forEach((t) => {
		delete e[t];
	}), delete e._chartjs);
}
function bc(e) {
	let t = new Set(e);
	return t.size === e.length ? e : Array.from(t);
}
var xc = function() {
	return typeof window > "u" ? function(e) {
		return e();
	} : window.requestAnimationFrame;
}();
function Sc(e, t) {
	let n = [], r = !1;
	return function(...i) {
		n = i, r || (r = !0, xc.call(window, () => {
			r = !1, e.apply(t, n);
		}));
	};
}
function Cc(e, t) {
	let n;
	return function(...r) {
		return t ? (clearTimeout(n), n = setTimeout(e, t, r)) : e.apply(this, r), t;
	};
}
var wc = (e) => e === "start" ? "left" : e === "end" ? "right" : "center", Tc = (e, t, n) => e === "start" ? t : e === "end" ? n : (t + n) / 2, Ec = (e) => e === 0 || e === 1, Dc = (e, t, n) => -(2 ** (10 * --e) * Math.sin((e - t) * Bs / n)), Oc = (e, t, n) => 2 ** (-10 * e) * Math.sin((e - t) * Bs / n) + 1, kc = {
	linear: (e) => e,
	easeInQuad: (e) => e * e,
	easeOutQuad: (e) => -e * (e - 2),
	easeInOutQuad: (e) => (e /= .5) < 1 ? .5 * e * e : -.5 * (--e * (e - 2) - 1),
	easeInCubic: (e) => e * e * e,
	easeOutCubic: (e) => --e * e * e + 1,
	easeInOutCubic: (e) => (e /= .5) < 1 ? .5 * e * e * e : .5 * ((e -= 2) * e * e + 2),
	easeInQuart: (e) => e * e * e * e,
	easeOutQuart: (e) => -(--e * e * e * e - 1),
	easeInOutQuart: (e) => (e /= .5) < 1 ? .5 * e * e * e * e : -.5 * ((e -= 2) * e * e * e - 2),
	easeInQuint: (e) => e * e * e * e * e,
	easeOutQuint: (e) => --e * e * e * e * e + 1,
	easeInOutQuint: (e) => (e /= .5) < 1 ? .5 * e * e * e * e * e : .5 * ((e -= 2) * e * e * e * e + 2),
	easeInSine: (e) => -Math.cos(e * Ws) + 1,
	easeOutSine: (e) => Math.sin(e * Ws),
	easeInOutSine: (e) => -.5 * (Math.cos(W * e) - 1),
	easeInExpo: (e) => e === 0 ? 0 : 2 ** (10 * (e - 1)),
	easeOutExpo: (e) => e === 1 ? 1 : -(2 ** (-10 * e)) + 1,
	easeInOutExpo: (e) => Ec(e) ? e : e < .5 ? .5 * 2 ** (10 * (e * 2 - 1)) : .5 * (-(2 ** (-10 * (e * 2 - 1))) + 2),
	easeInCirc: (e) => e >= 1 ? e : -(Math.sqrt(1 - e * e) - 1),
	easeOutCirc: (e) => Math.sqrt(1 - --e * e),
	easeInOutCirc: (e) => (e /= .5) < 1 ? -.5 * (Math.sqrt(1 - e * e) - 1) : .5 * (Math.sqrt(1 - (e -= 2) * e) + 1),
	easeInElastic: (e) => Ec(e) ? e : Dc(e, .075, .3),
	easeOutElastic: (e) => Ec(e) ? e : Oc(e, .075, .3),
	easeInOutElastic(e) {
		let t = .1125, n = .45;
		return Ec(e) ? e : e < .5 ? .5 * Dc(e * 2, t, n) : .5 + .5 * Oc(e * 2 - 1, t, n);
	},
	easeInBack(e) {
		return e * e * (2.70158 * e - 1.70158);
	},
	easeOutBack(e) {
		return --e * e * (2.70158 * e + 1.70158) + 1;
	},
	easeInOutBack(e) {
		let t = 1.70158;
		return (e /= .5) < 1 ? .5 * (e * e * (((t *= 1.525) + 1) * e - t)) : .5 * ((e -= 2) * e * (((t *= 1.525) + 1) * e + t) + 2);
	},
	easeInBounce: (e) => 1 - kc.easeOutBounce(1 - e),
	easeOutBounce(e) {
		let t = 7.5625, n = 2.75;
		return e < 1 / n ? t * e * e : e < 2 / n ? t * (e -= 1.5 / n) * e + .75 : e < 2.5 / n ? t * (e -= 2.25 / n) * e + .9375 : t * (e -= 2.625 / n) * e + .984375;
	},
	easeInOutBounce: (e) => e < .5 ? kc.easeInBounce(e * 2) * .5 : kc.easeOutBounce(e * 2 - 1) * .5 + .5
};
function Ac(e) {
	if (e && typeof e == "object") {
		let t = e.toString();
		return t === "[object CanvasPattern]" || t === "[object CanvasGradient]";
	}
	return !1;
}
function jc(e) {
	return Ac(e) ? e : new ys(e);
}
function Mc(e) {
	return Ac(e) ? e : new ys(e).saturate(.5).darken(.1).hexString();
}
var Nc = [
	"x",
	"y",
	"borderWidth",
	"radius",
	"tension"
], Pc = [
	"color",
	"borderColor",
	"backgroundColor"
];
function Fc(e) {
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
		_scriptable: (e) => e !== "onProgress" && e !== "onComplete" && e !== "fn"
	}), e.set("animations", {
		colors: {
			type: "color",
			properties: Pc
		},
		numbers: {
			type: "number",
			properties: Nc
		}
	}), e.describe("animations", { _fallback: "animation" }), e.set("transitions", {
		active: { animation: { duration: 400 } },
		resize: { animation: { duration: 0 } },
		show: { animations: {
			colors: { from: "transparent" },
			visible: {
				type: "boolean",
				duration: 0
			}
		} },
		hide: { animations: {
			colors: { to: "transparent" },
			visible: {
				type: "boolean",
				easing: "linear",
				fn: (e) => e | 0
			}
		} }
	});
}
function Ic(e) {
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
var Lc = /* @__PURE__ */ new Map();
function Rc(e, t) {
	t ||= {};
	let n = e + JSON.stringify(t), r = Lc.get(n);
	return r || (r = new Intl.NumberFormat(e, t), Lc.set(n, r)), r;
}
function zc(e, t, n) {
	return Rc(t, n).format(e);
}
var Bc = {
	values(e) {
		return R(e) ? e : "" + e;
	},
	numeric(e, t, n) {
		if (e === 0) return "0";
		let r = this.chart.options.locale, i, a = e;
		if (n.length > 1) {
			let t = Math.max(Math.abs(n[0].value), Math.abs(n[n.length - 1].value));
			(t < 1e-4 || t > 0x38d7ea4c68000) && (i = "scientific"), a = Vc(e, n);
		}
		let o = qs(Math.abs(a)), s = isNaN(o) ? 1 : Math.max(Math.min(-1 * Math.floor(o), 20), 0), c = {
			notation: i,
			minimumFractionDigits: s,
			maximumFractionDigits: s
		};
		return Object.assign(c, this.options.ticks.format), zc(e, r, c);
	},
	logarithmic(e, t, n) {
		if (e === 0) return "0";
		let r = n[t].significand || e / 10 ** Math.floor(qs(e));
		return [
			1,
			2,
			3,
			5,
			10,
			15
		].includes(r) || t > .8 * n.length ? Bc.numeric.call(this, e, t, n) : "";
	}
};
function Vc(e, t) {
	let n = t.length > 3 ? t[2].value - t[1].value : t[1].value - t[0].value;
	return Math.abs(n) >= 1 && e !== Math.floor(e) && (n = e - Math.floor(e)), n;
}
var Hc = { formatters: Bc };
function Uc(e) {
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
			tickWidth: (e, t) => t.lineWidth,
			tickColor: (e, t) => t.color,
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
			callback: Hc.formatters.values,
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
		_scriptable: (e) => !e.startsWith("before") && !e.startsWith("after") && e !== "callback" && e !== "parser",
		_indexable: (e) => e !== "borderDash" && e !== "tickBorderDash" && e !== "dash"
	}), e.describe("scales", { _fallback: "scale" }), e.describe("scale.ticks", {
		_scriptable: (e) => e !== "backdropPadding" && e !== "callback",
		_indexable: (e) => e !== "backdropPadding"
	});
}
var Wc = Object.create(null), Gc = Object.create(null);
function Kc(e, t) {
	if (!t) return e;
	let n = t.split(".");
	for (let t = 0, r = n.length; t < r; ++t) {
		let r = n[t];
		e = e[r] || (e[r] = Object.create(null));
	}
	return e;
}
function qc(e, t, n) {
	return typeof t == "string" ? Os(Kc(e, t), n) : Os(Kc(e, ""), t);
}
var G = /* #__PURE__ */ new class {
	constructor(e, t) {
		this.animation = void 0, this.backgroundColor = "rgba(0,0,0,0.1)", this.borderColor = "rgba(0,0,0,0.1)", this.color = "#666", this.datasets = {}, this.devicePixelRatio = (e) => e.chart.platform.getDevicePixelRatio(), this.elements = {}, this.events = [
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
		}, this.hover = {}, this.hoverBackgroundColor = (e, t) => Mc(t.backgroundColor), this.hoverBorderColor = (e, t) => Mc(t.borderColor), this.hoverColor = (e, t) => Mc(t.color), this.indexAxis = "x", this.interaction = {
			mode: "nearest",
			intersect: !0,
			includeInvisible: !1
		}, this.maintainAspectRatio = !0, this.onHover = null, this.onClick = null, this.parsing = !0, this.plugins = {}, this.responsive = !0, this.scale = void 0, this.scales = {}, this.showLine = !0, this.drawActiveElementsOnTop = !0, this.describe(e), this.apply(t);
	}
	set(e, t) {
		return qc(this, e, t);
	}
	get(e) {
		return Kc(this, e);
	}
	describe(e, t) {
		return qc(Gc, e, t);
	}
	override(e, t) {
		return qc(Wc, e, t);
	}
	route(e, t, n, r) {
		let i = Kc(this, e), a = Kc(this, n), o = "_" + t;
		Object.defineProperties(i, {
			[o]: {
				value: i[t],
				writable: !0
			},
			[t]: {
				enumerable: !0,
				get() {
					let e = this[o], t = a[r];
					return z(e) ? Object.assign({}, t, e) : V(e, t);
				},
				set(e) {
					this[o] = e;
				}
			}
		});
	}
	apply(e) {
		e.forEach((e) => e(this));
	}
}({
	_scriptable: (e) => !e.startsWith("on"),
	_indexable: (e) => e !== "events",
	hover: { _fallback: "interaction" },
	interaction: {
		_scriptable: !1,
		_indexable: !1
	}
}, [
	Fc,
	Ic,
	Uc
]);
function Jc(e) {
	return !e || L(e.size) || L(e.family) ? null : (e.style ? e.style + " " : "") + (e.weight ? e.weight + " " : "") + e.size + "px " + e.family;
}
function Yc(e, t, n, r, i) {
	let a = t[i];
	return a || (a = t[i] = e.measureText(i).width, n.push(i)), a > r && (r = a), r;
}
function Xc(e, t, n, r) {
	r ||= {};
	let i = r.data = r.data || {}, a = r.garbageCollect = r.garbageCollect || [];
	r.font !== t && (i = r.data = {}, a = r.garbageCollect = [], r.font = t), e.save(), e.font = t;
	let o = 0, s = n.length, c, l, u, d, f;
	for (c = 0; c < s; c++) if (d = n[c], d != null && !R(d)) o = Yc(e, i, a, o, d);
	else if (R(d)) for (l = 0, u = d.length; l < u; l++) f = d[l], f != null && !R(f) && (o = Yc(e, i, a, o, f));
	e.restore();
	let p = a.length / 2;
	if (p > n.length) {
		for (c = 0; c < p; c++) delete i[a[c]];
		a.splice(0, p);
	}
	return o;
}
function Zc(e, t, n) {
	let r = e.currentDevicePixelRatio, i = n === 0 ? 0 : Math.max(n / 2, .5);
	return Math.round((t - i) * r) / r + i;
}
function Qc(e, t) {
	!t && !e || (t ||= e.getContext("2d"), t.save(), t.resetTransform(), t.clearRect(0, 0, e.width, e.height), t.restore());
}
function $c(e, t, n, r) {
	el(e, t, n, r, null);
}
function el(e, t, n, r, i) {
	let a, o, s, c, l, u, d, f, p = t.pointStyle, m = t.rotation, h = t.radius, g = (m || 0) * Us;
	if (p && typeof p == "object" && (a = p.toString(), a === "[object HTMLImageElement]" || a === "[object HTMLCanvasElement]")) {
		e.save(), e.translate(n, r), e.rotate(g), e.drawImage(p, -p.width / 2, -p.height / 2, p.width, p.height), e.restore();
		return;
	}
	if (!(isNaN(h) || h <= 0)) {
		switch (e.beginPath(), p) {
			default:
				i ? e.ellipse(n, r, i / 2, h, 0, 0, Bs) : e.arc(n, r, h, 0, Bs), e.closePath();
				break;
			case "triangle":
				u = i ? i / 2 : h, e.moveTo(n + Math.sin(g) * u, r - Math.cos(g) * h), g += Ks, e.lineTo(n + Math.sin(g) * u, r - Math.cos(g) * h), g += Ks, e.lineTo(n + Math.sin(g) * u, r - Math.cos(g) * h), e.closePath();
				break;
			case "rectRounded":
				l = h * .516, c = h - l, o = Math.cos(g + Gs) * c, d = Math.cos(g + Gs) * (i ? i / 2 - l : c), s = Math.sin(g + Gs) * c, f = Math.sin(g + Gs) * (i ? i / 2 - l : c), e.arc(n - d, r - s, l, g - W, g - Ws), e.arc(n + f, r - o, l, g - Ws, g), e.arc(n + d, r + s, l, g, g + Ws), e.arc(n - f, r + o, l, g + Ws, g + W), e.closePath();
				break;
			case "rect":
				if (!m) {
					c = Math.SQRT1_2 * h, u = i ? i / 2 : c, e.rect(n - u, r - c, 2 * u, 2 * c);
					break;
				}
				g += Gs;
			case "rectRot":
				d = Math.cos(g) * (i ? i / 2 : h), o = Math.cos(g) * h, s = Math.sin(g) * h, f = Math.sin(g) * (i ? i / 2 : h), e.moveTo(n - d, r - s), e.lineTo(n + f, r - o), e.lineTo(n + d, r + s), e.lineTo(n - f, r + o), e.closePath();
				break;
			case "crossRot": g += Gs;
			case "cross":
				d = Math.cos(g) * (i ? i / 2 : h), o = Math.cos(g) * h, s = Math.sin(g) * h, f = Math.sin(g) * (i ? i / 2 : h), e.moveTo(n - d, r - s), e.lineTo(n + d, r + s), e.moveTo(n + f, r - o), e.lineTo(n - f, r + o);
				break;
			case "star":
				d = Math.cos(g) * (i ? i / 2 : h), o = Math.cos(g) * h, s = Math.sin(g) * h, f = Math.sin(g) * (i ? i / 2 : h), e.moveTo(n - d, r - s), e.lineTo(n + d, r + s), e.moveTo(n + f, r - o), e.lineTo(n - f, r + o), g += Gs, d = Math.cos(g) * (i ? i / 2 : h), o = Math.cos(g) * h, s = Math.sin(g) * h, f = Math.sin(g) * (i ? i / 2 : h), e.moveTo(n - d, r - s), e.lineTo(n + d, r + s), e.moveTo(n + f, r - o), e.lineTo(n - f, r + o);
				break;
			case "line":
				o = i ? i / 2 : Math.cos(g) * h, s = Math.sin(g) * h, e.moveTo(n - o, r - s), e.lineTo(n + o, r + s);
				break;
			case "dash":
				e.moveTo(n, r), e.lineTo(n + Math.cos(g) * (i ? i / 2 : h), r + Math.sin(g) * h);
				break;
			case !1:
				e.closePath();
				break;
		}
		e.fill(), t.borderWidth > 0 && e.stroke();
	}
}
function tl(e, t, n) {
	return n ||= .5, !t || e && e.x > t.left - n && e.x < t.right + n && e.y > t.top - n && e.y < t.bottom + n;
}
function nl(e, t) {
	e.save(), e.beginPath(), e.rect(t.left, t.top, t.right - t.left, t.bottom - t.top), e.clip();
}
function rl(e) {
	e.restore();
}
function il(e, t, n, r, i) {
	if (!t) return e.lineTo(n.x, n.y);
	if (i === "middle") {
		let r = (t.x + n.x) / 2;
		e.lineTo(r, t.y), e.lineTo(r, n.y);
	} else i === "after" == !!r ? e.lineTo(n.x, t.y) : e.lineTo(t.x, n.y);
	e.lineTo(n.x, n.y);
}
function al(e, t, n, r) {
	if (!t) return e.lineTo(n.x, n.y);
	e.bezierCurveTo(r ? t.cp1x : t.cp2x, r ? t.cp1y : t.cp2y, r ? n.cp2x : n.cp1x, r ? n.cp2y : n.cp1y, n.x, n.y);
}
function ol(e, t) {
	t.translation && e.translate(t.translation[0], t.translation[1]), L(t.rotation) || e.rotate(t.rotation), t.color && (e.fillStyle = t.color), t.textAlign && (e.textAlign = t.textAlign), t.textBaseline && (e.textBaseline = t.textBaseline);
}
function sl(e, t, n, r, i) {
	if (i.strikethrough || i.underline) {
		let a = e.measureText(r), o = t - a.actualBoundingBoxLeft, s = t + a.actualBoundingBoxRight, c = n - a.actualBoundingBoxAscent, l = n + a.actualBoundingBoxDescent, u = i.strikethrough ? (c + l) / 2 : l;
		e.strokeStyle = e.fillStyle, e.beginPath(), e.lineWidth = i.decorationWidth || 2, e.moveTo(o, u), e.lineTo(s, u), e.stroke();
	}
}
function cl(e, t) {
	let n = e.fillStyle;
	e.fillStyle = t.color, e.fillRect(t.left, t.top, t.width, t.height), e.fillStyle = n;
}
function ll(e, t, n, r, i, a = {}) {
	let o = R(t) ? t : [t], s = a.strokeWidth > 0 && a.strokeColor !== "", c, l;
	for (e.save(), e.font = i.string, ol(e, a), c = 0; c < o.length; ++c) l = o[c], a.backdrop && cl(e, a.backdrop), s && (a.strokeColor && (e.strokeStyle = a.strokeColor), L(a.strokeWidth) || (e.lineWidth = a.strokeWidth), e.strokeText(l, n, r, a.maxWidth)), e.fillText(l, n, r, a.maxWidth), sl(e, n, r, l, a), r += Number(i.lineHeight);
	e.restore();
}
function ul(e, t) {
	let { x: n, y: r, w: i, h: a, radius: o } = t;
	e.arc(n + o.topLeft, r + o.topLeft, o.topLeft, 1.5 * W, W, !0), e.lineTo(n, r + a - o.bottomLeft), e.arc(n + o.bottomLeft, r + a - o.bottomLeft, o.bottomLeft, W, Ws, !0), e.lineTo(n + i - o.bottomRight, r + a), e.arc(n + i - o.bottomRight, r + a - o.bottomRight, o.bottomRight, Ws, 0, !0), e.lineTo(n + i, r + o.topRight), e.arc(n + i - o.topRight, r + o.topRight, o.topRight, 0, -Ws, !0), e.lineTo(n + o.topLeft, r);
}
var dl = /^(normal|(\d+(?:\.\d+)?)(px|em|%)?)$/, fl = /^(normal|italic|initial|inherit|unset|(oblique( -?[0-9]?[0-9]deg)?))$/;
function pl(e, t) {
	let n = ("" + e).match(dl);
	if (!n || n[1] === "normal") return t * 1.2;
	switch (e = +n[2], n[3]) {
		case "px": return e;
		case "%":
			e /= 100;
			break;
	}
	return t * e;
}
var ml = (e) => +e || 0;
function hl(e, t) {
	let n = {}, r = z(t), i = r ? Object.keys(t) : t, a = z(e) ? r ? (n) => V(e[n], e[t[n]]) : (t) => e[t] : () => e;
	for (let e of i) n[e] = ml(a(e));
	return n;
}
function gl(e) {
	return hl(e, {
		top: "y",
		right: "x",
		bottom: "y",
		left: "x"
	});
}
function _l(e) {
	return hl(e, [
		"topLeft",
		"topRight",
		"bottomLeft",
		"bottomRight"
	]);
}
function vl(e) {
	let t = gl(e);
	return t.width = t.left + t.right, t.height = t.top + t.bottom, t;
}
function yl(e, t) {
	e ||= {}, t ||= G.font;
	let n = V(e.size, t.size);
	typeof n == "string" && (n = parseInt(n, 10));
	let r = V(e.style, t.style);
	r && !("" + r).match(fl) && (console.warn("Invalid font style specified: \"" + r + "\""), r = void 0);
	let i = {
		family: V(e.family, t.family),
		lineHeight: pl(V(e.lineHeight, t.lineHeight), n),
		size: n,
		style: r,
		weight: V(e.weight, t.weight),
		string: ""
	};
	return i.string = Jc(i), i;
}
function bl(e, t, n, r) {
	let i = !0, a, o, s;
	for (a = 0, o = e.length; a < o; ++a) if (s = e[a], s !== void 0 && (t !== void 0 && typeof s == "function" && (s = s(t), i = !1), n !== void 0 && R(s) && (s = s[n % s.length], i = !1), s !== void 0)) return r && !i && (r.cacheable = !1), s;
}
function xl(e, t, n) {
	let { min: r, max: i } = e, a = Cs(t, (i - r) / 2), o = (e, t) => n && e === 0 ? 0 : e + t;
	return {
		min: o(r, -Math.abs(a)),
		max: o(i, a)
	};
}
function Sl(e, t) {
	return Object.assign(Object.create(e), t);
}
function Cl(e, t = [""], n, r, i = () => e[0]) {
	let a = n || e;
	return r === void 0 && (r = zl("_fallback", e)), new Proxy({
		[Symbol.toStringTag]: "Object",
		_cacheable: !0,
		_scopes: e,
		_rootScopes: a,
		_fallback: r,
		_getTarget: i,
		override: (n) => Cl([n, ...e], t, a, r)
	}, {
		deleteProperty(t, n) {
			return delete t[n], delete t._keys, delete e[0][n], !0;
		},
		get(n, r) {
			return Ol(n, r, () => Rl(r, t, e, n));
		},
		getOwnPropertyDescriptor(e, t) {
			return Reflect.getOwnPropertyDescriptor(e._scopes[0], t);
		},
		getPrototypeOf() {
			return Reflect.getPrototypeOf(e[0]);
		},
		has(e, t) {
			return Bl(e).includes(t);
		},
		ownKeys(e) {
			return Bl(e);
		},
		set(e, t, n) {
			let r = e._storage ||= i();
			return e[t] = r[t] = n, delete e._keys, !0;
		}
	});
}
function wl(e, t, n, r) {
	let i = {
		_cacheable: !1,
		_proxy: e,
		_context: t,
		_subProxy: n,
		_stack: /* @__PURE__ */ new Set(),
		_descriptors: Tl(e, r),
		setContext: (t) => wl(e, t, n, r),
		override: (i) => wl(e.override(i), t, n, r)
	};
	return new Proxy(i, {
		deleteProperty(t, n) {
			return delete t[n], delete e[n], !0;
		},
		get(e, t, n) {
			return Ol(e, t, () => kl(e, t, n));
		},
		getOwnPropertyDescriptor(t, n) {
			return t._descriptors.allKeys ? Reflect.has(e, n) ? {
				enumerable: !0,
				configurable: !0
			} : void 0 : Reflect.getOwnPropertyDescriptor(e, n);
		},
		getPrototypeOf() {
			return Reflect.getPrototypeOf(e);
		},
		has(t, n) {
			return Reflect.has(e, n);
		},
		ownKeys() {
			return Reflect.ownKeys(e);
		},
		set(t, n, r) {
			return e[n] = r, delete t[n], !0;
		}
	});
}
function Tl(e, t = {
	scriptable: !0,
	indexable: !0
}) {
	let { _scriptable: n = t.scriptable, _indexable: r = t.indexable, _allKeys: i = t.allKeys } = e;
	return {
		allKeys: i,
		scriptable: n,
		indexable: r,
		isScriptable: Ls(n) ? n : () => n,
		isIndexable: Ls(r) ? r : () => r
	};
}
var El = (e, t) => e ? e + Fs(t) : t, Dl = (e, t) => z(t) && e !== "adapters" && (Object.getPrototypeOf(t) === null || t.constructor === Object);
function Ol(e, t, n) {
	if (Object.prototype.hasOwnProperty.call(e, t) || t === "constructor") return e[t];
	let r = n();
	return e[t] = r, r;
}
function kl(e, t, n) {
	let { _proxy: r, _context: i, _subProxy: a, _descriptors: o } = e, s = r[t];
	return Ls(s) && o.isScriptable(t) && (s = Al(t, s, e, n)), R(s) && s.length && (s = jl(t, s, e, o.isIndexable)), Dl(t, s) && (s = wl(s, i, a && a[t], o)), s;
}
function Al(e, t, n, r) {
	let { _proxy: i, _context: a, _subProxy: o, _stack: s } = n;
	if (s.has(e)) throw Error("Recursion detected: " + Array.from(s).join("->") + "->" + e);
	s.add(e);
	let c = t(a, o || r);
	return s.delete(e), Dl(e, c) && (c = Fl(i._scopes, i, e, c)), c;
}
function jl(e, t, n, r) {
	let { _proxy: i, _context: a, _subProxy: o, _descriptors: s } = n;
	if (a.index !== void 0 && r(e)) return t[a.index % t.length];
	if (z(t[0])) {
		let n = t, r = i._scopes.filter((e) => e !== n);
		t = [];
		for (let c of n) {
			let n = Fl(r, i, e, c);
			t.push(wl(n, a, o && o[e], s));
		}
	}
	return t;
}
function Ml(e, t, n) {
	return Ls(e) ? e(t, n) : e;
}
var Nl = (e, t) => e === !0 ? t : typeof e == "string" ? Ps(t, e) : void 0;
function Pl(e, t, n, r, i) {
	for (let a of t) {
		let t = Nl(n, a);
		if (t) {
			e.add(t);
			let a = Ml(t._fallback, n, i);
			if (a !== void 0 && a !== n && a !== r) return a;
		} else if (t === !1 && r !== void 0 && n !== r) return null;
	}
	return !1;
}
function Fl(e, t, n, r) {
	let i = t._rootScopes, a = Ml(t._fallback, n, r), o = [...e, ...i], s = /* @__PURE__ */ new Set();
	s.add(r);
	let c = Il(s, o, n, a || n, r);
	return c === null || a !== void 0 && a !== n && (c = Il(s, o, a, c, r), c === null) ? !1 : Cl(Array.from(s), [""], i, a, () => Ll(t, n, r));
}
function Il(e, t, n, r, i) {
	for (; n;) n = Pl(e, t, n, r, i);
	return n;
}
function Ll(e, t, n) {
	let r = e._getTarget();
	t in r || (r[t] = {});
	let i = r[t];
	return R(i) && z(n) ? n : i || {};
}
function Rl(e, t, n, r) {
	let i;
	for (let a of t) if (i = zl(El(a, e), n), i !== void 0) return Dl(e, i) ? Fl(n, r, e, i) : i;
}
function zl(e, t) {
	for (let n of t) {
		if (!n) continue;
		let t = n[e];
		if (t !== void 0) return t;
	}
}
function Bl(e) {
	let t = e._keys;
	return t ||= e._keys = Vl(e._scopes), t;
}
function Vl(e) {
	let t = /* @__PURE__ */ new Set();
	for (let n of e) for (let e of Object.keys(n).filter((e) => !e.startsWith("_"))) t.add(e);
	return Array.from(t);
}
var Hl = 2 ** -52 || 1e-14, Ul = (e, t) => t < e.length && !e[t].skip && e[t], Wl = (e) => e === "x" ? "y" : "x";
function Gl(e, t, n, r) {
	let i = e.skip ? t : e, a = t, o = n.skip ? t : n, s = oc(a, i), c = oc(o, a), l = s / (s + c), u = c / (s + c);
	l = isNaN(l) ? 0 : l, u = isNaN(u) ? 0 : u;
	let d = r * l, f = r * u;
	return {
		previous: {
			x: a.x - d * (o.x - i.x),
			y: a.y - d * (o.y - i.y)
		},
		next: {
			x: a.x + f * (o.x - i.x),
			y: a.y + f * (o.y - i.y)
		}
	};
}
function Kl(e, t, n) {
	let r = e.length, i, a, o, s, c, l = Ul(e, 0);
	for (let u = 0; u < r - 1; ++u) if (c = l, l = Ul(e, u + 1), !(!c || !l)) {
		if (Ys(t[u], 0, Hl)) {
			n[u] = n[u + 1] = 0;
			continue;
		}
		i = n[u] / t[u], a = n[u + 1] / t[u], s = i ** 2 + a ** 2, !(s <= 9) && (o = 3 / Math.sqrt(s), n[u] = i * o * t[u], n[u + 1] = a * o * t[u]);
	}
}
function ql(e, t, n = "x") {
	let r = Wl(n), i = e.length, a, o, s, c = Ul(e, 0);
	for (let l = 0; l < i; ++l) {
		if (o = s, s = c, c = Ul(e, l + 1), !s) continue;
		let i = s[n], u = s[r];
		o && (a = (i - o[n]) / 3, s[`cp1${n}`] = i - a, s[`cp1${r}`] = u - a * t[l]), c && (a = (c[n] - i) / 3, s[`cp2${n}`] = i + a, s[`cp2${r}`] = u + a * t[l]);
	}
}
function Jl(e, t = "x") {
	let n = Wl(t), r = e.length, i = Array(r).fill(0), a = Array(r), o, s, c, l = Ul(e, 0);
	for (o = 0; o < r; ++o) if (s = c, c = l, l = Ul(e, o + 1), c) {
		if (l) {
			let e = l[t] - c[t];
			i[o] = e === 0 ? 0 : (l[n] - c[n]) / e;
		}
		a[o] = s ? l ? Js(i[o - 1]) === Js(i[o]) ? (i[o - 1] + i[o]) / 2 : 0 : i[o - 1] : i[o];
	}
	Kl(e, i, a), ql(e, a, t);
}
function Yl(e, t, n) {
	return Math.max(Math.min(e, n), t);
}
function Xl(e, t) {
	let n, r, i, a, o, s = tl(e[0], t);
	for (n = 0, r = e.length; n < r; ++n) o = a, a = s, s = n < r - 1 && tl(e[n + 1], t), a && (i = e[n], o && (i.cp1x = Yl(i.cp1x, t.left, t.right), i.cp1y = Yl(i.cp1y, t.top, t.bottom)), s && (i.cp2x = Yl(i.cp2x, t.left, t.right), i.cp2y = Yl(i.cp2y, t.top, t.bottom)));
}
function Zl(e, t, n, r, i) {
	let a, o, s, c;
	if (t.spanGaps && (e = e.filter((e) => !e.skip)), t.cubicInterpolationMode === "monotone") Jl(e, i);
	else {
		let n = r ? e[e.length - 1] : e[0];
		for (a = 0, o = e.length; a < o; ++a) s = e[a], c = Gl(n, s, e[Math.min(a + 1, o - +!r) % o], t.tension), s.cp1x = c.previous.x, s.cp1y = c.previous.y, s.cp2x = c.next.x, s.cp2y = c.next.y, n = s;
	}
	t.capBezierPoints && Xl(e, n);
}
function Ql() {
	return typeof window < "u" && typeof document < "u";
}
function $l(e) {
	let t = e.parentNode;
	return t && t.toString() === "[object ShadowRoot]" && (t = t.host), t;
}
function eu(e, t, n) {
	let r;
	return typeof e == "string" ? (r = parseInt(e, 10), e.indexOf("%") !== -1 && (r = r / 100 * t.parentNode[n])) : r = e, r;
}
var tu = (e) => e.ownerDocument.defaultView.getComputedStyle(e, null);
function nu(e, t) {
	return tu(e).getPropertyValue(t);
}
var ru = [
	"top",
	"right",
	"bottom",
	"left"
];
function iu(e, t, n) {
	let r = {};
	n = n ? "-" + n : "";
	for (let i = 0; i < 4; i++) {
		let a = ru[i];
		r[a] = parseFloat(e[t + "-" + a + n]) || 0;
	}
	return r.width = r.left + r.right, r.height = r.top + r.bottom, r;
}
var au = (e, t, n) => (e > 0 || t > 0) && (!n || !n.shadowRoot);
function ou(e, t) {
	let n = e.touches, r = n && n.length ? n[0] : e, { offsetX: i, offsetY: a } = r, o = !1, s, c;
	if (au(i, a, e.target)) s = i, c = a;
	else {
		let e = t.getBoundingClientRect();
		s = r.clientX - e.left, c = r.clientY - e.top, o = !0;
	}
	return {
		x: s,
		y: c,
		box: o
	};
}
function su(e, t) {
	if ("native" in e) return e;
	let { canvas: n, currentDevicePixelRatio: r } = t, i = tu(n), a = i.boxSizing === "border-box", o = iu(i, "padding"), s = iu(i, "border", "width"), { x: c, y: l, box: u } = ou(e, n), d = o.left + (u && s.left), f = o.top + (u && s.top), { width: p, height: m } = t;
	return a && (p -= o.width + s.width, m -= o.height + s.height), {
		x: Math.round((c - d) / p * n.width / r),
		y: Math.round((l - f) / m * n.height / r)
	};
}
function cu(e, t, n) {
	let r, i;
	if (t === void 0 || n === void 0) {
		let a = e && $l(e);
		if (!a) t = e.clientWidth, n = e.clientHeight;
		else {
			let e = a.getBoundingClientRect(), o = tu(a), s = iu(o, "border", "width"), c = iu(o, "padding");
			t = e.width - c.width - s.width, n = e.height - c.height - s.height, r = eu(o.maxWidth, a, "clientWidth"), i = eu(o.maxHeight, a, "clientHeight");
		}
	}
	return {
		width: t,
		height: n,
		maxWidth: r || Hs,
		maxHeight: i || Hs
	};
}
var lu = (e) => Math.round(e * 10) / 10;
function uu(e, t, n, r) {
	let i = tu(e), a = iu(i, "margin"), o = eu(i.maxWidth, e, "clientWidth") || Hs, s = eu(i.maxHeight, e, "clientHeight") || Hs, c = cu(e, t, n), { width: l, height: u } = c;
	if (i.boxSizing === "content-box") {
		let e = iu(i, "border", "width"), t = iu(i, "padding");
		l -= t.width + e.width, u -= t.height + e.height;
	}
	return l = Math.max(0, l - a.width), u = Math.max(0, r ? l / r : u - a.height), l = lu(Math.min(l, o, c.maxWidth)), u = lu(Math.min(u, s, c.maxHeight)), l && !u && (u = lu(l / 2)), (t !== void 0 || n !== void 0) && r && c.height && u > c.height && (u = c.height, l = lu(Math.floor(u * r))), {
		width: l,
		height: u
	};
}
function du(e, t, n) {
	let r = t || 1, i = lu(e.height * r), a = lu(e.width * r);
	e.height = lu(e.height), e.width = lu(e.width);
	let o = e.canvas;
	return o.style && (n || !o.style.height && !o.style.width) && (o.style.height = `${e.height}px`, o.style.width = `${e.width}px`), e.currentDevicePixelRatio !== r || o.height !== i || o.width !== a ? (e.currentDevicePixelRatio = r, o.height = i, o.width = a, e.ctx.setTransform(r, 0, 0, r, 0, 0), !0) : !1;
}
var fu = function() {
	let e = !1;
	try {
		let t = { get passive() {
			return e = !0, !1;
		} };
		Ql() && (window.addEventListener("test", null, t), window.removeEventListener("test", null, t));
	} catch {}
	return e;
}();
function pu(e, t) {
	let n = nu(e, t), r = n && n.match(/^(\d+)(\.\d+)?px$/);
	return r ? +r[1] : void 0;
}
function mu(e, t, n, r) {
	return {
		x: e.x + n * (t.x - e.x),
		y: e.y + n * (t.y - e.y)
	};
}
function hu(e, t, n, r) {
	return {
		x: e.x + n * (t.x - e.x),
		y: r === "middle" ? n < .5 ? e.y : t.y : r === "after" ? n < 1 ? e.y : t.y : n > 0 ? t.y : e.y
	};
}
function gu(e, t, n, r) {
	let i = {
		x: e.cp2x,
		y: e.cp2y
	}, a = {
		x: t.cp1x,
		y: t.cp1y
	}, o = mu(e, i, n), s = mu(i, a, n), c = mu(a, t, n);
	return mu(mu(o, s, n), mu(s, c, n), n);
}
var _u = function(e, t) {
	return {
		x(n) {
			return e + e + t - n;
		},
		setWidth(e) {
			t = e;
		},
		textAlign(e) {
			return e === "center" ? e : e === "right" ? "left" : "right";
		},
		xPlus(e, t) {
			return e - t;
		},
		leftForLtr(e, t) {
			return e - t;
		}
	};
}, vu = function() {
	return {
		x(e) {
			return e;
		},
		setWidth(e) {},
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
function yu(e, t, n) {
	return e ? _u(t, n) : vu();
}
function bu(e, t) {
	let n, r;
	(t === "ltr" || t === "rtl") && (n = e.canvas.style, r = [n.getPropertyValue("direction"), n.getPropertyPriority("direction")], n.setProperty("direction", t, "important"), e.prevTextDirection = r);
}
function xu(e, t) {
	t !== void 0 && (delete e.prevTextDirection, e.canvas.style.setProperty("direction", t[0], t[1]));
}
function Su(e) {
	return e === "angle" ? {
		between: lc,
		compare: sc,
		normalize: cc
	} : {
		between: fc,
		compare: (e, t) => e - t,
		normalize: (e) => e
	};
}
function Cu({ start: e, end: t, count: n, loop: r, style: i }) {
	return {
		start: e % n,
		end: t % n,
		loop: r && (t - e + 1) % n === 0,
		style: i
	};
}
function wu(e, t, n) {
	let { property: r, start: i, end: a } = n, { between: o, normalize: s } = Su(r), c = t.length, { start: l, end: u, loop: d } = e, f, p;
	if (d) {
		for (l += c, u += c, f = 0, p = c; f < p && o(s(t[l % c][r]), i, a); ++f) l--, u--;
		l %= c, u %= c;
	}
	return u < l && (u += c), {
		start: l,
		end: u,
		loop: d,
		style: e.style
	};
}
function Tu(e, t, n) {
	if (!n) return [e];
	let { property: r, start: i, end: a } = n, o = t.length, { compare: s, between: c, normalize: l } = Su(r), { start: u, end: d, loop: f, style: p } = wu(e, t, n), m = [], h = !1, g = null, _, v, y, b = () => c(i, y, _) && s(i, y) !== 0, x = () => s(a, _) === 0 || c(a, y, _), S = () => h || b(), C = () => !h || x();
	for (let e = u, n = u; e <= d; ++e) v = t[e % o], !v.skip && (_ = l(v[r]), _ !== y && (h = c(_, i, a), g === null && S() && (g = s(_, i) === 0 ? e : n), g !== null && C() && (m.push(Cu({
		start: g,
		end: e,
		loop: f,
		count: o,
		style: p
	})), g = null), n = e, y = _));
	return g !== null && m.push(Cu({
		start: g,
		end: d,
		loop: f,
		count: o,
		style: p
	})), m;
}
function Eu(e, t) {
	let n = [], r = e.segments;
	for (let i = 0; i < r.length; i++) {
		let a = Tu(r[i], e.points, t);
		a.length && n.push(...a);
	}
	return n;
}
function Du(e, t, n, r) {
	let i = 0, a = t - 1;
	if (n && !r) for (; i < t && !e[i].skip;) i++;
	for (; i < t && e[i].skip;) i++;
	for (i %= t, n && (a += i); a > i && e[a % t].skip;) a--;
	return a %= t, {
		start: i,
		end: a
	};
}
function Ou(e, t, n, r) {
	let i = e.length, a = [], o = t, s = e[t], c;
	for (c = t + 1; c <= n; ++c) {
		let n = e[c % i];
		n.skip || n.stop ? s.skip || (r = !1, a.push({
			start: t % i,
			end: (c - 1) % i,
			loop: r
		}), t = o = n.stop ? c : null) : (o = c, s.skip && (t = c)), s = n;
	}
	return o !== null && a.push({
		start: t % i,
		end: o % i,
		loop: r
	}), a;
}
function ku(e, t) {
	let n = e.points, r = e.options.spanGaps, i = n.length;
	if (!i) return [];
	let a = !!e._loop, { start: o, end: s } = Du(n, i, a, r);
	return r === !0 ? Au(e, [{
		start: o,
		end: s,
		loop: a
	}], n, t) : Au(e, Ou(n, o, s < o ? s + i : s, !!e._fullLoop && o === 0 && s === i - 1), n, t);
}
function Au(e, t, n, r) {
	return !r || !r.setContext || !n ? t : ju(e, t, n, r);
}
function ju(e, t, n, r) {
	let i = e._chart.getContext(), a = Mu(e.options), { _datasetIndex: o, options: { spanGaps: s } } = e, c = n.length, l = [], u = a, d = t[0].start, f = d;
	function p(e, t, r, i) {
		let a = s ? -1 : 1;
		if (e !== t) {
			for (e += c; n[e % c].skip;) e -= a;
			for (; n[t % c].skip;) t += a;
			e % c !== t % c && (l.push({
				start: e % c,
				end: t % c,
				loop: r,
				style: i
			}), u = i, d = t % c);
		}
	}
	for (let e of t) {
		d = s ? d : e.start;
		let t = n[d % c], a;
		for (f = d + 1; f <= e.end; f++) {
			let s = n[f % c];
			a = Mu(r.setContext(Sl(i, {
				type: "segment",
				p0: t,
				p1: s,
				p0DataIndex: (f - 1) % c,
				p1DataIndex: f % c,
				datasetIndex: o
			}))), Nu(a, u) && p(d, f - 1, e.loop, u), t = s, u = a;
		}
		d < f - 1 && p(d, f - 1, e.loop, u);
	}
	return l;
}
function Mu(e) {
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
function Nu(e, t) {
	if (!t) return !1;
	let n = [], r = function(e, t) {
		return Ac(t) ? (n.includes(t) || n.push(t), n.indexOf(t)) : t;
	};
	return JSON.stringify(e, r) !== JSON.stringify(t, r);
}
function Pu(e, t, n) {
	return e.options.clip ? e[n] : t[n];
}
function Fu(e, t) {
	let { xScale: n, yScale: r } = e;
	return n && r ? {
		left: Pu(n, t, "left"),
		right: Pu(n, t, "right"),
		top: Pu(r, t, "top"),
		bottom: Pu(r, t, "bottom")
	} : t;
}
function Iu(e, t) {
	let n = t._clip;
	if (n.disabled) return !1;
	let r = Fu(t, e.chartArea);
	return {
		left: n.left === !1 ? 0 : r.left - (n.left === !0 ? 0 : n.left),
		right: n.right === !1 ? e.width : r.right + (n.right === !0 ? 0 : n.right),
		top: n.top === !1 ? 0 : r.top - (n.top === !0 ? 0 : n.top),
		bottom: n.bottom === !1 ? e.height : r.bottom + (n.bottom === !0 ? 0 : n.bottom)
	};
}
var Lu = /* #__PURE__ */ new class {
	constructor() {
		this._request = null, this._charts = /* @__PURE__ */ new Map(), this._running = !1, this._lastDate = void 0;
	}
	_notify(e, t, n, r) {
		let i = t.listeners[r], a = t.duration;
		i.forEach((r) => r({
			chart: e,
			initial: t.initial,
			numSteps: a,
			currentStep: Math.min(n - t.start, a)
		}));
	}
	_refresh() {
		this._request ||= (this._running = !0, xc.call(window, () => {
			this._update(), this._request = null, this._running && this._refresh();
		}));
	}
	_update(e = Date.now()) {
		let t = 0;
		this._charts.forEach((n, r) => {
			if (!n.running || !n.items.length) return;
			let i = n.items, a = i.length - 1, o = !1, s;
			for (; a >= 0; --a) s = i[a], s._active ? (s._total > n.duration && (n.duration = s._total), s.tick(e), o = !0) : (i[a] = i[i.length - 1], i.pop());
			o && (r.draw(), this._notify(r, n, e, "progress")), i.length || (n.running = !1, this._notify(r, n, e, "complete"), n.initial = !1), t += i.length;
		}), this._lastDate = e, t === 0 && (this._running = !1);
	}
	_getAnims(e) {
		let t = this._charts, n = t.get(e);
		return n || (n = {
			running: !1,
			initial: !0,
			items: [],
			listeners: {
				complete: [],
				progress: []
			}
		}, t.set(e, n)), n;
	}
	listen(e, t, n) {
		this._getAnims(e).listeners[t].push(n);
	}
	add(e, t) {
		!t || !t.length || this._getAnims(e).items.push(...t);
	}
	has(e) {
		return this._getAnims(e).items.length > 0;
	}
	start(e) {
		let t = this._charts.get(e);
		t && (t.running = !0, t.start = Date.now(), t.duration = t.items.reduce((e, t) => Math.max(e, t._duration), 0), this._refresh());
	}
	running(e) {
		if (!this._running) return !1;
		let t = this._charts.get(e);
		return !(!t || !t.running || !t.items.length);
	}
	stop(e) {
		let t = this._charts.get(e);
		if (!t || !t.items.length) return;
		let n = t.items, r = n.length - 1;
		for (; r >= 0; --r) n[r].cancel();
		t.items = [], this._notify(e, t, Date.now(), "complete");
	}
	remove(e) {
		return this._charts.delete(e);
	}
}(), Ru = "transparent", zu = {
	boolean(e, t, n) {
		return n > .5 ? t : e;
	},
	color(e, t, n) {
		let r = jc(e || Ru), i = r.valid && jc(t || Ru);
		return i && i.valid ? i.mix(r, n).hexString() : t;
	},
	number(e, t, n) {
		return e + (t - e) * n;
	}
}, Bu = class {
	constructor(e, t, n, r) {
		let i = t[n];
		r = bl([
			e.to,
			r,
			i,
			e.from
		]);
		let a = bl([
			e.from,
			i,
			r
		]);
		this._active = !0, this._fn = e.fn || zu[e.type || typeof a], this._easing = kc[e.easing] || kc.linear, this._start = Math.floor(Date.now() + (e.delay || 0)), this._duration = this._total = Math.floor(e.duration), this._loop = !!e.loop, this._target = t, this._prop = n, this._from = a, this._to = r, this._promises = void 0;
	}
	active() {
		return this._active;
	}
	update(e, t, n) {
		if (this._active) {
			this._notify(!1);
			let r = this._target[this._prop], i = n - this._start, a = this._duration - i;
			this._start = n, this._duration = Math.floor(Math.max(a, e.duration)), this._total += i, this._loop = !!e.loop, this._to = bl([
				e.to,
				t,
				r,
				e.from
			]), this._from = bl([
				e.from,
				r,
				t
			]);
		}
	}
	cancel() {
		this._active && (this.tick(Date.now()), this._active = !1, this._notify(!1));
	}
	tick(e) {
		let t = e - this._start, n = this._duration, r = this._prop, i = this._from, a = this._loop, o = this._to, s;
		if (this._active = i !== o && (a || t < n), !this._active) {
			this._target[r] = o, this._notify(!0);
			return;
		}
		if (t < 0) {
			this._target[r] = i;
			return;
		}
		s = t / n % 2, s = a && s > 1 ? 2 - s : s, s = this._easing(Math.min(1, Math.max(0, s))), this._target[r] = this._fn(i, o, s);
	}
	wait() {
		let e = this._promises ||= [];
		return new Promise((t, n) => {
			e.push({
				res: t,
				rej: n
			});
		});
	}
	_notify(e) {
		let t = e ? "res" : "rej", n = this._promises || [];
		for (let e = 0; e < n.length; e++) n[e][t]();
	}
}, Vu = class {
	constructor(e, t) {
		this._chart = e, this._properties = /* @__PURE__ */ new Map(), this.configure(t);
	}
	configure(e) {
		if (!z(e)) return;
		let t = Object.keys(G.animation), n = this._properties;
		Object.getOwnPropertyNames(e).forEach((r) => {
			let i = e[r];
			if (!z(i)) return;
			let a = {};
			for (let e of t) a[e] = i[e];
			(R(i.properties) && i.properties || [r]).forEach((e) => {
				(e === r || !n.has(e)) && n.set(e, a);
			});
		});
	}
	_animateOptions(e, t) {
		let n = t.options, r = Uu(e, n);
		if (!r) return [];
		let i = this._createAnimations(r, n);
		return n.$shared && Hu(e.options.$animations, n).then(() => {
			e.options = n;
		}, () => {}), i;
	}
	_createAnimations(e, t) {
		let n = this._properties, r = [], i = e.$animations ||= {}, a = Object.keys(t), o = Date.now(), s;
		for (s = a.length - 1; s >= 0; --s) {
			let c = a[s];
			if (c.charAt(0) === "$") continue;
			if (c === "options") {
				r.push(...this._animateOptions(e, t));
				continue;
			}
			let l = t[c], u = i[c], d = n.get(c);
			if (u) if (d && u.active()) {
				u.update(d, l, o);
				continue;
			} else u.cancel();
			if (!d || !d.duration) {
				e[c] = l;
				continue;
			}
			i[c] = u = new Bu(d, e, c, l), r.push(u);
		}
		return r;
	}
	update(e, t) {
		if (this._properties.size === 0) {
			Object.assign(e, t);
			return;
		}
		let n = this._createAnimations(e, t);
		if (n.length) return Lu.add(this._chart, n), !0;
	}
};
function Hu(e, t) {
	let n = [], r = Object.keys(t);
	for (let t = 0; t < r.length; t++) {
		let i = e[r[t]];
		i && i.active() && n.push(i.wait());
	}
	return Promise.all(n);
}
function Uu(e, t) {
	if (!t) return;
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
function Wu(e, t) {
	let n = e && e.options || {}, r = n.reverse, i = n.min === void 0 ? t : 0, a = n.max === void 0 ? t : 0;
	return {
		start: r ? a : i,
		end: r ? i : a
	};
}
function Gu(e, t, n) {
	if (n === !1) return !1;
	let r = Wu(e, n), i = Wu(t, n);
	return {
		top: i.end,
		right: r.end,
		bottom: i.start,
		left: r.start
	};
}
function Ku(e) {
	let t, n, r, i;
	return z(e) ? (t = e.top, n = e.right, r = e.bottom, i = e.left) : t = n = r = i = e, {
		top: t,
		right: n,
		bottom: r,
		left: i,
		disabled: e === !1
	};
}
function qu(e, t) {
	let n = [], r = e._getSortedDatasetMetas(t), i, a;
	for (i = 0, a = r.length; i < a; ++i) n.push(r[i].index);
	return n;
}
function Ju(e, t, n, r = {}) {
	let i = e.keys, a = r.mode === "single", o, s, c, l;
	if (t === null) return;
	let u = !1;
	for (o = 0, s = i.length; o < s; ++o) {
		if (c = +i[o], c === n) {
			if (u = !0, r.all) continue;
			break;
		}
		l = e.values[c], B(l) && (a || t === 0 || Js(t) === Js(l)) && (t += l);
	}
	return !u && !r.all ? 0 : t;
}
function Yu(e, t) {
	let { iScale: n, vScale: r } = t, i = n.axis === "x" ? "x" : "y", a = r.axis === "x" ? "x" : "y", o = Object.keys(e), s = Array(o.length), c, l, u;
	for (c = 0, l = o.length; c < l; ++c) u = o[c], s[c] = {
		[i]: u,
		[a]: e[u]
	};
	return s;
}
function Xu(e, t) {
	let n = e && e.options.stacked;
	return n || n === void 0 && t.stack !== void 0;
}
function Zu(e, t, n) {
	return `${e.id}.${t.id}.${n.stack || n.type}`;
}
function Qu(e) {
	let { min: t, max: n, minDefined: r, maxDefined: i } = e.getUserBounds();
	return {
		min: r ? t : -Infinity,
		max: i ? n : Infinity
	};
}
function $u(e, t, n) {
	let r = e[t] || (e[t] = {});
	return r[n] || (r[n] = {});
}
function ed(e, t, n, r) {
	for (let i of t.getMatchingVisibleMetas(r).reverse()) {
		let t = e[i.index];
		if (n && t > 0 || !n && t < 0) return i.index;
	}
	return null;
}
function td(e, t) {
	let { chart: n, _cachedMeta: r } = e, i = n._stacks ||= {}, { iScale: a, vScale: o, index: s } = r, c = a.axis, l = o.axis, u = Zu(a, o, r), d = t.length, f;
	for (let e = 0; e < d; ++e) {
		let n = t[e], { [c]: a, [l]: d } = n, p = n._stacks ||= {};
		f = p[l] = $u(i, u, a), f[s] = d, f._top = ed(f, o, !0, r.type), f._bottom = ed(f, o, !1, r.type);
		let m = f._visualValues ||= {};
		m[s] = d;
	}
}
function nd(e, t) {
	let n = e.scales;
	return Object.keys(n).filter((e) => n[e].axis === t).shift();
}
function rd(e, t) {
	return Sl(e, {
		active: !1,
		dataset: void 0,
		datasetIndex: t,
		index: t,
		mode: "default",
		type: "dataset"
	});
}
function id(e, t, n) {
	return Sl(e, {
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
function ad(e, t) {
	let n = e.controller.index, r = e.vScale && e.vScale.axis;
	if (r) {
		t ||= e._parsed;
		for (let e of t) {
			let t = e._stacks;
			if (!t || t[r] === void 0 || t[r][n] === void 0) return;
			delete t[r][n], t[r]._visualValues !== void 0 && t[r]._visualValues[n] !== void 0 && delete t[r]._visualValues[n];
		}
	}
}
var od = (e) => e === "reset" || e === "none", sd = (e, t) => t ? e : Object.assign({}, e), cd = (e, t, n) => e && !t.hidden && t._stacked && {
	keys: qu(n, !0),
	values: null
}, ld = class {
	static defaults = {};
	static datasetElementType = null;
	static dataElementType = null;
	constructor(e, t) {
		this.chart = e, this._ctx = e.ctx, this.index = t, this._cachedDataOpts = {}, this._cachedMeta = this.getMeta(), this._type = this._cachedMeta.type, this.options = void 0, this._parsing = !1, this._data = void 0, this._objectData = void 0, this._sharedOptions = void 0, this._drawStart = void 0, this._drawCount = void 0, this.enableOptionSharing = !1, this.supportsDecimation = !1, this.$context = void 0, this._syncList = [], this.datasetElementType = new.target.datasetElementType, this.dataElementType = new.target.dataElementType, this.initialize();
	}
	initialize() {
		let e = this._cachedMeta;
		this.configure(), this.linkScales(), e._stacked = Xu(e.vScale, e), this.addElements(), this.options.fill && !this.chart.isPluginEnabled("filler") && console.warn("Tried to use the 'fill' option without the 'Filler' plugin enabled. Please import and register the 'Filler' plugin and make sure it is not disabled in the options");
	}
	updateIndex(e) {
		this.index !== e && ad(this._cachedMeta), this.index = e;
	}
	linkScales() {
		let e = this.chart, t = this._cachedMeta, n = this.getDataset(), r = (e, t, n, r) => e === "x" ? t : e === "r" ? r : n, i = t.xAxisID = V(n.xAxisID, nd(e, "x")), a = t.yAxisID = V(n.yAxisID, nd(e, "y")), o = t.rAxisID = V(n.rAxisID, nd(e, "r")), s = t.indexAxis, c = t.iAxisID = r(s, i, a, o), l = t.vAxisID = r(s, a, i, o);
		t.xScale = this.getScaleForId(i), t.yScale = this.getScaleForId(a), t.rScale = this.getScaleForId(o), t.iScale = this.getScaleForId(c), t.vScale = this.getScaleForId(l);
	}
	getDataset() {
		return this.chart.data.datasets[this.index];
	}
	getMeta() {
		return this.chart.getDatasetMeta(this.index);
	}
	getScaleForId(e) {
		return this.chart.scales[e];
	}
	_getOtherScale(e) {
		let t = this._cachedMeta;
		return e === t.iScale ? t.vScale : t.iScale;
	}
	reset() {
		this._update("reset");
	}
	_destroy() {
		let e = this._cachedMeta;
		this._data && yc(this._data, this), e._stacked && ad(e);
	}
	_dataCheck() {
		let e = this.getDataset(), t = e.data ||= [], n = this._data;
		if (z(t)) {
			let e = this._cachedMeta;
			this._data = Yu(t, e);
		} else if (n !== t) {
			if (n) {
				yc(n, this);
				let e = this._cachedMeta;
				ad(e), e._parsed = [];
			}
			t && Object.isExtensible(t) && vc(t, this), this._syncList = [], this._data = t;
		}
	}
	addElements() {
		let e = this._cachedMeta;
		this._dataCheck(), this.datasetElementType && (e.dataset = new this.datasetElementType());
	}
	buildOrUpdateElements(e) {
		let t = this._cachedMeta, n = this.getDataset(), r = !1;
		this._dataCheck();
		let i = t._stacked;
		t._stacked = Xu(t.vScale, t), t.stack !== n.stack && (r = !0, ad(t), t.stack = n.stack), this._resyncElements(e), (r || i !== t._stacked) && (td(this, t._parsed), t._stacked = Xu(t.vScale, t));
	}
	configure() {
		let e = this.chart.config, t = e.datasetScopeKeys(this._type), n = e.getOptionScopes(this.getDataset(), t, !0);
		this.options = e.createResolver(n, this.getContext()), this._parsing = this.options.parsing, this._cachedDataOpts = {};
	}
	parse(e, t) {
		let { _cachedMeta: n, _data: r } = this, { iScale: i, _stacked: a } = n, o = i.axis, s = e === 0 && t === r.length ? !0 : n._sorted, c = e > 0 && n._parsed[e - 1], l, u, d;
		if (this._parsing === !1) n._parsed = r, n._sorted = !0, d = r;
		else {
			d = R(r[e]) ? this.parseArrayData(n, r, e, t) : z(r[e]) ? this.parseObjectData(n, r, e, t) : this.parsePrimitiveData(n, r, e, t);
			let i = () => u[o] === null || c && u[o] < c[o];
			for (l = 0; l < t; ++l) n._parsed[l + e] = u = d[l], s && (i() && (s = !1), c = u);
			n._sorted = s;
		}
		a && td(this, d);
	}
	parsePrimitiveData(e, t, n, r) {
		let { iScale: i, vScale: a } = e, o = i.axis, s = a.axis, c = i.getLabels(), l = i === a, u = Array(r), d, f, p;
		for (d = 0, f = r; d < f; ++d) p = d + n, u[d] = {
			[o]: l || i.parse(c[p], p),
			[s]: a.parse(t[p], p)
		};
		return u;
	}
	parseArrayData(e, t, n, r) {
		let { xScale: i, yScale: a } = e, o = Array(r), s, c, l, u;
		for (s = 0, c = r; s < c; ++s) l = s + n, u = t[l], o[s] = {
			x: i.parse(u[0], l),
			y: a.parse(u[1], l)
		};
		return o;
	}
	parseObjectData(e, t, n, r) {
		let { xScale: i, yScale: a } = e, { xAxisKey: o = "x", yAxisKey: s = "y" } = this._parsing, c = Array(r), l, u, d, f;
		for (l = 0, u = r; l < u; ++l) d = l + n, f = t[d], c[l] = {
			x: i.parse(Ps(f, o), d),
			y: a.parse(Ps(f, s), d)
		};
		return c;
	}
	getParsed(e) {
		return this._cachedMeta._parsed[e];
	}
	getDataElement(e) {
		return this._cachedMeta.data[e];
	}
	applyStack(e, t, n) {
		let r = this.chart, i = this._cachedMeta, a = t[e.axis];
		return Ju({
			keys: qu(r, !0),
			values: t._stacks[e.axis]._visualValues
		}, a, i.index, { mode: n });
	}
	updateRangeFromParsed(e, t, n, r) {
		let i = n[t.axis], a = i === null ? NaN : i, o = r && n._stacks[t.axis];
		r && o && (r.values = o, a = Ju(r, i, this._cachedMeta.index)), e.min = Math.min(e.min, a), e.max = Math.max(e.max, a);
	}
	getMinMax(e, t) {
		let n = this._cachedMeta, r = n._parsed, i = n._sorted && e === n.iScale, a = r.length, o = this._getOtherScale(e), s = cd(t, n, this.chart), c = {
			min: Infinity,
			max: -Infinity
		}, { min: l, max: u } = Qu(o), d, f;
		function p() {
			f = r[d];
			let t = f[o.axis];
			return !B(f[e.axis]) || l > t || u < t;
		}
		for (d = 0; d < a && !(!p() && (this.updateRangeFromParsed(c, e, f, s), i)); ++d);
		if (i) {
			for (d = a - 1; d >= 0; --d) if (!p()) {
				this.updateRangeFromParsed(c, e, f, s);
				break;
			}
		}
		return c;
	}
	getAllParsedValues(e) {
		let t = this._cachedMeta._parsed, n = [], r, i, a;
		for (r = 0, i = t.length; r < i; ++r) a = t[r][e.axis], B(a) && n.push(a);
		return n;
	}
	getMaxOverflow() {
		return !1;
	}
	getLabelAndValue(e) {
		let t = this._cachedMeta, n = t.iScale, r = t.vScale, i = this.getParsed(e);
		return {
			label: n ? "" + n.getLabelForValue(i[n.axis]) : "",
			value: r ? "" + r.getLabelForValue(i[r.axis]) : ""
		};
	}
	_update(e) {
		let t = this._cachedMeta;
		this.update(e || "default"), t._clip = Ku(V(this.options.clip, Gu(t.xScale, t.yScale, this.getMaxOverflow())));
	}
	update(e) {}
	draw() {
		let e = this._ctx, t = this.chart, n = this._cachedMeta, r = n.data || [], i = t.chartArea, a = [], o = this._drawStart || 0, s = this._drawCount || r.length - o, c = this.options.drawActiveElementsOnTop, l;
		for (n.dataset && n.dataset.draw(e, i, o, s), l = o; l < o + s; ++l) {
			let t = r[l];
			t.hidden || (t.active && c ? a.push(t) : t.draw(e, i));
		}
		for (l = 0; l < a.length; ++l) a[l].draw(e, i);
	}
	getStyle(e, t) {
		let n = t ? "active" : "default";
		return e === void 0 && this._cachedMeta.dataset ? this.resolveDatasetElementOptions(n) : this.resolveDataElementOptions(e || 0, n);
	}
	getContext(e, t, n) {
		let r = this.getDataset(), i;
		if (e >= 0 && e < this._cachedMeta.data.length) {
			let t = this._cachedMeta.data[e];
			i = t.$context ||= id(this.getContext(), e, t), i.parsed = this.getParsed(e), i.raw = r.data[e], i.index = i.dataIndex = e;
		} else i = this.$context ||= rd(this.chart.getContext(), this.index), i.dataset = r, i.index = i.datasetIndex = this.index;
		return i.active = !!t, i.mode = n, i;
	}
	resolveDatasetElementOptions(e) {
		return this._resolveElementOptions(this.datasetElementType.id, e);
	}
	resolveDataElementOptions(e, t) {
		return this._resolveElementOptions(this.dataElementType.id, t, e);
	}
	_resolveElementOptions(e, t = "default", n) {
		let r = t === "active", i = this._cachedDataOpts, a = e + "-" + t, o = i[a], s = this.enableOptionSharing && Is(n);
		if (o) return sd(o, s);
		let c = this.chart.config, l = c.datasetElementScopeKeys(this._type, e), u = r ? [
			`${e}Hover`,
			"hover",
			e,
			""
		] : [e, ""], d = c.getOptionScopes(this.getDataset(), l), f = Object.keys(G.elements[e]), p = c.resolveNamedOptions(d, f, () => this.getContext(n, r, t), u);
		return p.$shared && (p.$shared = s, i[a] = Object.freeze(sd(p, s))), p;
	}
	_resolveAnimations(e, t, n) {
		let r = this.chart, i = this._cachedDataOpts, a = `animation-${t}`, o = i[a];
		if (o) return o;
		let s;
		if (r.options.animation !== !1) {
			let r = this.chart.config, i = r.datasetAnimationScopeKeys(this._type, t), a = r.getOptionScopes(this.getDataset(), i);
			s = r.createResolver(a, this.getContext(e, n, t));
		}
		let c = new Vu(r, s && s.animations);
		return s && s._cacheable && (i[a] = Object.freeze(c)), c;
	}
	getSharedOptions(e) {
		if (e.$shared) return this._sharedOptions ||= Object.assign({}, e);
	}
	includeOptions(e, t) {
		return !t || od(e) || this.chart._animationsDisabled;
	}
	_getSharedOptions(e, t) {
		let n = this.resolveDataElementOptions(e, t), r = this._sharedOptions, i = this.getSharedOptions(n), a = this.includeOptions(t, i) || i !== r;
		return this.updateSharedOptions(i, t, n), {
			sharedOptions: i,
			includeOptions: a
		};
	}
	updateElement(e, t, n, r) {
		od(r) ? Object.assign(e, n) : this._resolveAnimations(t, r).update(e, n);
	}
	updateSharedOptions(e, t, n) {
		e && !od(t) && this._resolveAnimations(void 0, t).update(e, n);
	}
	_setStyle(e, t, n, r) {
		e.active = r;
		let i = this.getStyle(t, r);
		this._resolveAnimations(t, n, r).update(e, { options: !r && this.getSharedOptions(i) || i });
	}
	removeHoverStyle(e, t, n) {
		this._setStyle(e, n, "active", !1);
	}
	setHoverStyle(e, t, n) {
		this._setStyle(e, n, "active", !0);
	}
	_removeDatasetHoverStyle() {
		let e = this._cachedMeta.dataset;
		e && this._setStyle(e, void 0, "active", !1);
	}
	_setDatasetHoverStyle() {
		let e = this._cachedMeta.dataset;
		e && this._setStyle(e, void 0, "active", !0);
	}
	_resyncElements(e) {
		let t = this._data, n = this._cachedMeta.data;
		for (let [e, t, n] of this._syncList) this[e](t, n);
		this._syncList = [];
		let r = n.length, i = t.length, a = Math.min(i, r);
		a && this.parse(0, a), i > r ? this._insertElements(r, i - r, e) : i < r && this._removeElements(i, r - i);
	}
	_insertElements(e, t, n = !0) {
		let r = this._cachedMeta, i = r.data, a = e + t, o, s = (e) => {
			for (e.length += t, o = e.length - 1; o >= a; o--) e[o] = e[o - t];
		};
		for (s(i), o = e; o < a; ++o) i[o] = new this.dataElementType();
		this._parsing && s(r._parsed), this.parse(e, t), n && this.updateElements(i, e, t, "reset");
	}
	updateElements(e, t, n, r) {}
	_removeElements(e, t) {
		let n = this._cachedMeta;
		if (this._parsing) {
			let r = n._parsed.splice(e, t);
			n._stacked && ad(n, r);
		}
		n.data.splice(e, t);
	}
	_sync(e) {
		if (this._parsing) this._syncList.push(e);
		else {
			let [t, n, r] = e;
			this[t](n, r);
		}
		this.chart._dataChanges.push([this.index, ...e]);
	}
	_onDataPush() {
		let e = arguments.length;
		this._sync([
			"_insertElements",
			this.getDataset().data.length - e,
			e
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
	_onDataSplice(e, t) {
		t && this._sync([
			"_removeElements",
			e,
			t
		]);
		let n = arguments.length - 2;
		n && this._sync([
			"_insertElements",
			e,
			n
		]);
	}
	_onDataUnshift() {
		this._sync([
			"_insertElements",
			0,
			arguments.length
		]);
	}
};
function ud(e, t) {
	if (!e._cache.$bar) {
		let n = e.getMatchingVisibleMetas(t), r = [];
		for (let t = 0, i = n.length; t < i; t++) r = r.concat(n[t].controller.getAllParsedValues(e));
		e._cache.$bar = bc(r.sort((e, t) => e - t));
	}
	return e._cache.$bar;
}
function dd(e) {
	let t = e.iScale, n = ud(t, e.type), r = t._length, i, a, o, s, c = () => {
		o === 32767 || o === -32768 || (Is(s) && (r = Math.min(r, Math.abs(o - s) || r)), s = o);
	};
	for (i = 0, a = n.length; i < a; ++i) o = t.getPixelForValue(n[i]), c();
	for (s = void 0, i = 0, a = t.ticks.length; i < a; ++i) o = t.getPixelForTick(i), c();
	return r;
}
function fd(e, t, n, r) {
	let i = n.barThickness, a, o;
	return L(i) ? (a = t.min * n.categoryPercentage, o = n.barPercentage) : (a = i * r, o = 1), {
		chunk: a / r,
		ratio: o,
		start: t.pixels[e] - a / 2
	};
}
function pd(e, t, n, r) {
	let i = t.pixels, a = i[e], o = e > 0 ? i[e - 1] : null, s = e < i.length - 1 ? i[e + 1] : null, c = n.categoryPercentage;
	o === null && (o = a - (s === null ? t.end - t.start : s - a)), s === null && (s = a + a - o);
	let l = a - (a - Math.min(o, s)) / 2 * c;
	return {
		chunk: Math.abs(s - o) / 2 * c / r,
		ratio: n.barPercentage,
		start: l
	};
}
function md(e, t, n, r) {
	let i = n.parse(e[0], r), a = n.parse(e[1], r), o = Math.min(i, a), s = Math.max(i, a), c = o, l = s;
	Math.abs(o) > Math.abs(s) && (c = s, l = o), t[n.axis] = l, t._custom = {
		barStart: c,
		barEnd: l,
		start: i,
		end: a,
		min: o,
		max: s
	};
}
function hd(e, t, n, r) {
	return R(e) ? md(e, t, n, r) : t[n.axis] = n.parse(e, r), t;
}
function gd(e, t, n, r) {
	let i = e.iScale, a = e.vScale, o = i.getLabels(), s = i === a, c = [], l, u, d, f;
	for (l = n, u = n + r; l < u; ++l) f = t[l], d = {}, d[i.axis] = s || i.parse(o[l], l), c.push(hd(f, d, a, l));
	return c;
}
function _d(e) {
	return e && e.barStart !== void 0 && e.barEnd !== void 0;
}
function vd(e, t, n) {
	return e === 0 ? (t.isHorizontal() ? 1 : -1) * (t.min >= n ? 1 : -1) : Js(e);
}
function yd(e) {
	let t, n, r, i, a;
	return e.horizontal ? (t = e.base > e.x, n = "left", r = "right") : (t = e.base < e.y, n = "bottom", r = "top"), t ? (i = "end", a = "start") : (i = "start", a = "end"), {
		start: n,
		end: r,
		reverse: t,
		top: i,
		bottom: a
	};
}
function bd(e, t, n, r) {
	let i = t.borderSkipped, a = {};
	if (!i) {
		e.borderSkipped = a;
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
	let { start: o, end: s, reverse: c, top: l, bottom: u } = yd(e);
	i === "middle" && n && (e.enableBorderRadius = !0, (n._top || 0) === r ? i = l : (n._bottom || 0) === r ? i = u : (a[xd(u, o, s, c)] = !0, i = l)), a[xd(i, o, s, c)] = !0, e.borderSkipped = a;
}
function xd(e, t, n, r) {
	return r ? (e = Sd(e, t, n), e = Cd(e, n, t)) : e = Cd(e, t, n), e;
}
function Sd(e, t, n) {
	return e === t ? n : e === n ? t : e;
}
function Cd(e, t, n) {
	return e === "start" ? t : e === "end" ? n : e;
}
function wd(e, { inflateAmount: t }, n) {
	e.inflateAmount = t === "auto" ? n === 1 ? .33 : 0 : t;
}
var Td = class extends ld {
	static id = "bar";
	static defaults = {
		datasetElementType: !1,
		dataElementType: "bar",
		categoryPercentage: .8,
		barPercentage: .9,
		grouped: !0,
		animations: { numbers: {
			type: "number",
			properties: [
				"x",
				"y",
				"base",
				"width",
				"height"
			]
		} }
	};
	static overrides = { scales: {
		_index_: {
			type: "category",
			offset: !0,
			grid: { offset: !0 }
		},
		_value_: {
			type: "linear",
			beginAtZero: !0
		}
	} };
	parsePrimitiveData(e, t, n, r) {
		return gd(e, t, n, r);
	}
	parseArrayData(e, t, n, r) {
		return gd(e, t, n, r);
	}
	parseObjectData(e, t, n, r) {
		let { iScale: i, vScale: a } = e, { xAxisKey: o = "x", yAxisKey: s = "y" } = this._parsing, c = i.axis === "x" ? o : s, l = a.axis === "x" ? o : s, u = [], d, f, p, m;
		for (d = n, f = n + r; d < f; ++d) m = t[d], p = {}, p[i.axis] = i.parse(Ps(m, c), d), u.push(hd(Ps(m, l), p, a, d));
		return u;
	}
	updateRangeFromParsed(e, t, n, r) {
		super.updateRangeFromParsed(e, t, n, r);
		let i = n._custom;
		i && t === this._cachedMeta.vScale && (e.min = Math.min(e.min, i.min), e.max = Math.max(e.max, i.max));
	}
	getMaxOverflow() {
		return 0;
	}
	getLabelAndValue(e) {
		let { iScale: t, vScale: n } = this._cachedMeta, r = this.getParsed(e), i = r._custom, a = _d(i) ? "[" + i.start + ", " + i.end + "]" : "" + n.getLabelForValue(r[n.axis]);
		return {
			label: "" + t.getLabelForValue(r[t.axis]),
			value: a
		};
	}
	initialize() {
		this.enableOptionSharing = !0, super.initialize();
		let e = this._cachedMeta;
		e.stack = this.getDataset().stack;
	}
	update(e) {
		let t = this._cachedMeta;
		this.updateElements(t.data, 0, t.data.length, e);
	}
	updateElements(e, t, n, r) {
		let i = r === "reset", { index: a, _cachedMeta: { vScale: o } } = this, s = o.getBasePixel(), c = o.isHorizontal(), l = this._getRuler(), { sharedOptions: u, includeOptions: d } = this._getSharedOptions(t, r);
		for (let f = t; f < t + n; f++) {
			let t = this.getParsed(f), n = i || L(t[o.axis]) ? {
				base: s,
				head: s
			} : this._calculateBarValuePixels(f), p = this._calculateBarIndexPixels(f, l), m = (t._stacks || {})[o.axis], h = {
				horizontal: c,
				base: n.base,
				enableBorderRadius: !m || _d(t._custom) || a === m._top || a === m._bottom,
				x: c ? n.head : p.center,
				y: c ? p.center : n.head,
				height: c ? p.size : Math.abs(n.size),
				width: c ? Math.abs(n.size) : p.size
			};
			d && (h.options = u || this.resolveDataElementOptions(f, e[f].active ? "active" : r));
			let g = h.options || e[f].options;
			bd(h, g, m, a), wd(h, g, l.ratio), this.updateElement(e[f], f, h, r);
		}
	}
	_getStacks(e, t) {
		let { iScale: n } = this._cachedMeta, r = n.getMatchingVisibleMetas(this._type).filter((e) => e.controller.options.grouped), i = n.options.stacked, a = [], o = this._cachedMeta.controller.getParsed(t), s = o && o[n.axis], c = (e) => {
			let t = e._parsed.find((e) => e[n.axis] === s), r = t && t[e.vScale.axis];
			if (L(r) || isNaN(r)) return !0;
		};
		for (let n of r) if (!(t !== void 0 && c(n)) && ((i === !1 || a.indexOf(n.stack) === -1 || i === void 0 && n.stack === void 0) && a.push(n.stack), n.index === e)) break;
		return a.length || a.push(void 0), a;
	}
	_getStackCount(e) {
		return this._getStacks(void 0, e).length;
	}
	_getAxisCount() {
		return this._getAxis().length;
	}
	getFirstScaleIdForIndexAxis() {
		let e = this.chart.scales, t = this.chart.options.indexAxis;
		return Object.keys(e).filter((n) => e[n].axis === t).shift();
	}
	_getAxis() {
		let e = {}, t = this.getFirstScaleIdForIndexAxis();
		for (let n of this.chart.data.datasets) e[V(this.chart.options.indexAxis === "x" ? n.xAxisID : n.yAxisID, t)] = !0;
		return Object.keys(e);
	}
	_getStackIndex(e, t, n) {
		let r = this._getStacks(e, n), i = t === void 0 ? -1 : r.indexOf(t);
		return i === -1 ? r.length - 1 : i;
	}
	_getRuler() {
		let e = this.options, t = this._cachedMeta, n = t.iScale, r = [], i, a;
		for (i = 0, a = t.data.length; i < a; ++i) r.push(n.getPixelForValue(this.getParsed(i)[n.axis], i));
		let o = e.barThickness;
		return {
			min: o || dd(t),
			pixels: r,
			start: n._startPixel,
			end: n._endPixel,
			stackCount: this._getStackCount(),
			scale: n,
			grouped: e.grouped,
			ratio: o ? 1 : e.categoryPercentage * e.barPercentage
		};
	}
	_calculateBarValuePixels(e) {
		let { _cachedMeta: { vScale: t, _stacked: n, index: r }, options: { base: i, minBarLength: a } } = this, o = i || 0, s = this.getParsed(e), c = s._custom, l = _d(c), u = s[t.axis], d = 0, f = n ? this.applyStack(t, s, n) : u, p, m;
		f !== u && (d = f - u, f = u), l && (u = c.barStart, f = c.barEnd - c.barStart, u !== 0 && Js(u) !== Js(c.barEnd) && (d = 0), d += u);
		let h = !L(i) && !l ? i : d, g = t.getPixelForValue(h);
		if (p = this.chart.getDataVisibility(e) ? t.getPixelForValue(d + f) : g, m = p - g, Math.abs(m) < a) {
			m = vd(m, t, o) * a, u === o && (g -= m / 2);
			let e = t.getPixelForDecimal(0), i = t.getPixelForDecimal(1);
			g = Math.max(Math.min(g, Math.max(e, i)), Math.min(e, i)), p = g + m, n && !l && (s._stacks[t.axis]._visualValues[r] = t.getValueForPixel(p) - t.getValueForPixel(g));
		}
		if (g === t.getPixelForValue(o)) {
			let e = Js(m) * t.getLineWidthForValue(o) / 2;
			g += e, m -= e;
		}
		return {
			size: m,
			base: g,
			head: p,
			center: p + m / 2
		};
	}
	_calculateBarIndexPixels(e, t) {
		let n = t.scale, r = this.options, i = r.skipNull, a = V(r.maxBarThickness, Infinity), o, s, c = this._getAxisCount();
		if (t.grouped) {
			let n = i ? this._getStackCount(e) : t.stackCount, l = r.barThickness === "flex" ? pd(e, t, r, n * c) : fd(e, t, r, n * c), u = this.chart.options.indexAxis === "x" ? this.getDataset().xAxisID : this.getDataset().yAxisID, d = this._getAxis().indexOf(V(u, this.getFirstScaleIdForIndexAxis())), f = this._getStackIndex(this.index, this._cachedMeta.stack, i ? e : void 0) + d;
			o = l.start + l.chunk * f + l.chunk / 2, s = Math.min(a, l.chunk * l.ratio);
		} else o = n.getPixelForValue(this.getParsed(e)[n.axis], e), s = Math.min(a, t.min * t.ratio);
		return {
			base: o - s / 2,
			head: o + s / 2,
			center: o,
			size: s
		};
	}
	draw() {
		let e = this._cachedMeta, t = e.vScale, n = e.data, r = n.length, i = 0;
		for (; i < r; ++i) this.getParsed(i)[t.axis] !== null && !n[i].hidden && n[i].draw(this._ctx);
	}
};
function Ed() {
	throw Error("This method is not implemented: Check that a complete date adapter is provided.");
}
var Dd = { _date: class e {
	static override(t) {
		Object.assign(e.prototype, t);
	}
	options;
	constructor(e) {
		this.options = e || {};
	}
	init() {}
	formats() {
		return Ed();
	}
	parse() {
		return Ed();
	}
	format() {
		return Ed();
	}
	add() {
		return Ed();
	}
	diff() {
		return Ed();
	}
	startOf() {
		return Ed();
	}
	endOf() {
		return Ed();
	}
} };
function Od(e, t, n, r) {
	let { controller: i, data: a, _sorted: o } = e, s = i._cachedMeta.iScale, c = e.dataset && e.dataset.options ? e.dataset.options.spanGaps : null;
	if (s && t === s.axis && t !== "r" && o && a.length) {
		let o = s._reversePixels ? hc : mc;
		if (!r) {
			let r = o(a, t, n);
			if (c) {
				let { vScale: t } = i._cachedMeta, { _parsed: n } = e, a = n.slice(0, r.lo + 1).reverse().findIndex((e) => !L(e[t.axis]));
				r.lo -= Math.max(0, a);
				let o = n.slice(r.hi).findIndex((e) => !L(e[t.axis]));
				r.hi += Math.max(0, o);
			}
			return r;
		} else if (i._sharedOptions) {
			let e = a[0], r = typeof e.getRange == "function" && e.getRange(t);
			if (r) {
				let e = o(a, t, n - r), i = o(a, t, n + r);
				return {
					lo: e.lo,
					hi: i.hi
				};
			}
		}
	}
	return {
		lo: 0,
		hi: a.length - 1
	};
}
function kd(e, t, n, r, i) {
	let a = e.getSortedVisibleDatasetMetas(), o = n[t];
	for (let e = 0, n = a.length; e < n; ++e) {
		let { index: n, data: s } = a[e], { lo: c, hi: l } = Od(a[e], t, o, i);
		for (let e = c; e <= l; ++e) {
			let t = s[e];
			t.skip || r(t, n, e);
		}
	}
}
function Ad(e) {
	let t = e.indexOf("x") !== -1, n = e.indexOf("y") !== -1;
	return function(e, r) {
		let i = t ? Math.abs(e.x - r.x) : 0, a = n ? Math.abs(e.y - r.y) : 0;
		return Math.sqrt(i ** 2 + a ** 2);
	};
}
function jd(e, t, n, r, i) {
	let a = [];
	return !i && !e.isPointInArea(t) || kd(e, n, t, function(n, o, s) {
		!i && !tl(n, e.chartArea, 0) || n.inRange(t.x, t.y, r) && a.push({
			element: n,
			datasetIndex: o,
			index: s
		});
	}, !0), a;
}
function Md(e, t, n, r) {
	let i = [];
	function a(e, n, a) {
		let { startAngle: o, endAngle: s } = e.getProps(["startAngle", "endAngle"], r), { angle: c } = ac(e, {
			x: t.x,
			y: t.y
		});
		lc(c, o, s) && i.push({
			element: e,
			datasetIndex: n,
			index: a
		});
	}
	return kd(e, n, t, a), i;
}
function Nd(e, t, n, r, i, a) {
	let o = [], s = Ad(n), c = Infinity;
	function l(n, l, u) {
		let d = n.inRange(t.x, t.y, i);
		if (r && !d) return;
		let f = n.getCenterPoint(i);
		if (!(a || e.isPointInArea(f)) && !d) return;
		let p = s(t, f);
		p < c ? (o = [{
			element: n,
			datasetIndex: l,
			index: u
		}], c = p) : p === c && o.push({
			element: n,
			datasetIndex: l,
			index: u
		});
	}
	return kd(e, n, t, l), o;
}
function Pd(e, t, n, r, i, a) {
	return !a && !e.isPointInArea(t) ? [] : n === "r" && !r ? Md(e, t, n, i) : Nd(e, t, n, r, i, a);
}
function Fd(e, t, n, r, i) {
	let a = [], o = n === "x" ? "inXRange" : "inYRange", s = !1;
	return kd(e, n, t, (e, r, c) => {
		e[o] && e[o](t[n], i) && (a.push({
			element: e,
			datasetIndex: r,
			index: c
		}), s ||= e.inRange(t.x, t.y, i));
	}), r && !s ? [] : a;
}
var Id = {
	evaluateInteractionItems: kd,
	modes: {
		index(e, t, n, r) {
			let i = su(t, e), a = n.axis || "x", o = n.includeInvisible || !1, s = n.intersect ? jd(e, i, a, r, o) : Pd(e, i, a, !1, r, o), c = [];
			return s.length ? (e.getSortedVisibleDatasetMetas().forEach((e) => {
				let t = s[0].index, n = e.data[t];
				n && !n.skip && c.push({
					element: n,
					datasetIndex: e.index,
					index: t
				});
			}), c) : [];
		},
		dataset(e, t, n, r) {
			let i = su(t, e), a = n.axis || "xy", o = n.includeInvisible || !1, s = n.intersect ? jd(e, i, a, r, o) : Pd(e, i, a, !1, r, o);
			if (s.length > 0) {
				let t = s[0].datasetIndex, n = e.getDatasetMeta(t).data;
				s = [];
				for (let e = 0; e < n.length; ++e) s.push({
					element: n[e],
					datasetIndex: t,
					index: e
				});
			}
			return s;
		},
		point(e, t, n, r) {
			return jd(e, su(t, e), n.axis || "xy", r, n.includeInvisible || !1);
		},
		nearest(e, t, n, r) {
			let i = su(t, e), a = n.axis || "xy", o = n.includeInvisible || !1;
			return Pd(e, i, a, n.intersect, r, o);
		},
		x(e, t, n, r) {
			return Fd(e, su(t, e), "x", n.intersect, r);
		},
		y(e, t, n, r) {
			return Fd(e, su(t, e), "y", n.intersect, r);
		}
	}
}, Ld = [
	"left",
	"top",
	"right",
	"bottom"
];
function Rd(e, t) {
	return e.filter((e) => e.pos === t);
}
function zd(e, t) {
	return e.filter((e) => Ld.indexOf(e.pos) === -1 && e.box.axis === t);
}
function Bd(e, t) {
	return e.sort((e, n) => {
		let r = t ? n : e, i = t ? e : n;
		return r.weight === i.weight ? r.index - i.index : r.weight - i.weight;
	});
}
function Vd(e) {
	let t = [], n, r, i, a, o, s;
	for (n = 0, r = (e || []).length; n < r; ++n) i = e[n], {position: a, options: {stack: o, stackWeight: s = 1}} = i, t.push({
		index: n,
		box: i,
		pos: a,
		horizontal: i.isHorizontal(),
		weight: i.weight,
		stack: o && a + o,
		stackWeight: s
	});
	return t;
}
function Hd(e) {
	let t = {};
	for (let n of e) {
		let { stack: e, pos: r, stackWeight: i } = n;
		if (!e || !Ld.includes(r)) continue;
		let a = t[e] || (t[e] = {
			count: 0,
			placed: 0,
			weight: 0,
			size: 0
		});
		a.count++, a.weight += i;
	}
	return t;
}
function Ud(e, t) {
	let n = Hd(e), { vBoxMaxWidth: r, hBoxMaxHeight: i } = t, a, o, s;
	for (a = 0, o = e.length; a < o; ++a) {
		s = e[a];
		let { fullSize: o } = s.box, c = n[s.stack], l = c && s.stackWeight / c.weight;
		s.horizontal ? (s.width = l ? l * r : o && t.availableWidth, s.height = i) : (s.width = r, s.height = l ? l * i : o && t.availableHeight);
	}
	return n;
}
function Wd(e) {
	let t = Vd(e), n = Bd(t.filter((e) => e.box.fullSize), !0), r = Bd(Rd(t, "left"), !0), i = Bd(Rd(t, "right")), a = Bd(Rd(t, "top"), !0), o = Bd(Rd(t, "bottom")), s = zd(t, "x"), c = zd(t, "y");
	return {
		fullSize: n,
		leftAndTop: r.concat(a),
		rightAndBottom: i.concat(c).concat(o).concat(s),
		chartArea: Rd(t, "chartArea"),
		vertical: r.concat(i).concat(c),
		horizontal: a.concat(o).concat(s)
	};
}
function Gd(e, t, n, r) {
	return Math.max(e[n], t[n]) + Math.max(e[r], t[r]);
}
function Kd(e, t) {
	e.top = Math.max(e.top, t.top), e.left = Math.max(e.left, t.left), e.bottom = Math.max(e.bottom, t.bottom), e.right = Math.max(e.right, t.right);
}
function qd(e, t, n, r) {
	let { pos: i, box: a } = n, o = e.maxPadding;
	if (!z(i)) {
		n.size && (e[i] -= n.size);
		let t = r[n.stack] || {
			size: 0,
			count: 1
		};
		t.size = Math.max(t.size, n.horizontal ? a.height : a.width), n.size = t.size / t.count, e[i] += n.size;
	}
	a.getPadding && Kd(o, a.getPadding());
	let s = Math.max(0, t.outerWidth - Gd(o, e, "left", "right")), c = Math.max(0, t.outerHeight - Gd(o, e, "top", "bottom")), l = s !== e.w, u = c !== e.h;
	return e.w = s, e.h = c, n.horizontal ? {
		same: l,
		other: u
	} : {
		same: u,
		other: l
	};
}
function Jd(e) {
	let t = e.maxPadding;
	function n(n) {
		let r = Math.max(t[n] - e[n], 0);
		return e[n] += r, r;
	}
	e.y += n("top"), e.x += n("left"), n("right"), n("bottom");
}
function Yd(e, t) {
	let n = t.maxPadding;
	function r(e) {
		let r = {
			left: 0,
			top: 0,
			right: 0,
			bottom: 0
		};
		return e.forEach((e) => {
			r[e] = Math.max(t[e], n[e]);
		}), r;
	}
	return r(e ? ["left", "right"] : ["top", "bottom"]);
}
function Xd(e, t, n, r) {
	let i = [], a, o, s, c, l, u;
	for (a = 0, o = e.length, l = 0; a < o; ++a) {
		s = e[a], c = s.box, c.update(s.width || t.w, s.height || t.h, Yd(s.horizontal, t));
		let { same: o, other: d } = qd(t, n, s, r);
		l |= o && i.length, u ||= d, c.fullSize || i.push(s);
	}
	return l && Xd(i, t, n, r) || u;
}
function Zd(e, t, n, r, i) {
	e.top = n, e.left = t, e.right = t + r, e.bottom = n + i, e.width = r, e.height = i;
}
function Qd(e, t, n, r) {
	let i = n.padding, { x: a, y: o } = t;
	for (let s of e) {
		let e = s.box, c = r[s.stack] || {
			count: 1,
			placed: 0,
			weight: 1
		}, l = s.stackWeight / c.weight || 1;
		if (s.horizontal) {
			let r = t.w * l, a = c.size || e.height;
			Is(c.start) && (o = c.start), e.fullSize ? Zd(e, i.left, o, n.outerWidth - i.right - i.left, a) : Zd(e, t.left + c.placed, o, r, a), c.start = o, c.placed += r, o = e.bottom;
		} else {
			let r = t.h * l, o = c.size || e.width;
			Is(c.start) && (a = c.start), e.fullSize ? Zd(e, a, i.top, o, n.outerHeight - i.bottom - i.top) : Zd(e, a, t.top + c.placed, o, r), c.start = a, c.placed += r, a = e.right;
		}
	}
	t.x = a, t.y = o;
}
var $d = {
	addBox(e, t) {
		e.boxes ||= [], t.fullSize = t.fullSize || !1, t.position = t.position || "top", t.weight = t.weight || 0, t._layers = t._layers || function() {
			return [{
				z: 0,
				draw(e) {
					t.draw(e);
				}
			}];
		}, e.boxes.push(t);
	},
	removeBox(e, t) {
		let n = e.boxes ? e.boxes.indexOf(t) : -1;
		n !== -1 && e.boxes.splice(n, 1);
	},
	configure(e, t, n) {
		t.fullSize = n.fullSize, t.position = n.position, t.weight = n.weight;
	},
	update(e, t, n, r) {
		if (!e) return;
		let i = vl(e.options.layout.padding), a = Math.max(t - i.width, 0), o = Math.max(n - i.height, 0), s = Wd(e.boxes), c = s.vertical, l = s.horizontal;
		U(e.boxes, (e) => {
			typeof e.beforeLayout == "function" && e.beforeLayout();
		});
		let u = c.reduce((e, t) => t.box.options && t.box.options.display === !1 ? e : e + 1, 0) || 1, d = Object.freeze({
			outerWidth: t,
			outerHeight: n,
			padding: i,
			availableWidth: a,
			availableHeight: o,
			vBoxMaxWidth: a / 2 / u,
			hBoxMaxHeight: o / 2
		}), f = Object.assign({}, i);
		Kd(f, vl(r));
		let p = Object.assign({
			maxPadding: f,
			w: a,
			h: o,
			x: i.left,
			y: i.top
		}, i), m = Ud(c.concat(l), d);
		Xd(s.fullSize, p, d, m), Xd(c, p, d, m), Xd(l, p, d, m) && Xd(c, p, d, m), Jd(p), Qd(s.leftAndTop, p, d, m), p.x += p.w, p.y += p.h, Qd(s.rightAndBottom, p, d, m), e.chartArea = {
			left: p.left,
			top: p.top,
			right: p.left + p.w,
			bottom: p.top + p.h,
			height: p.h,
			width: p.w
		}, U(s.chartArea, (t) => {
			let n = t.box;
			Object.assign(n, e.chartArea), n.update(p.w, p.h, {
				left: 0,
				top: 0,
				right: 0,
				bottom: 0
			});
		});
	}
}, ef = class {
	acquireContext(e, t) {}
	releaseContext(e) {
		return !1;
	}
	addEventListener(e, t, n) {}
	removeEventListener(e, t, n) {}
	getDevicePixelRatio() {
		return 1;
	}
	getMaximumSize(e, t, n, r) {
		return t = Math.max(0, t || e.width), n ||= e.height, {
			width: t,
			height: Math.max(0, r ? Math.floor(t / r) : n)
		};
	}
	isAttached(e) {
		return !0;
	}
	updateConfig(e) {}
}, tf = class extends ef {
	acquireContext(e) {
		return e && e.getContext && e.getContext("2d") || null;
	}
	updateConfig(e) {
		e.options.animation = !1;
	}
}, nf = "$chartjs", rf = {
	touchstart: "mousedown",
	touchmove: "mousemove",
	touchend: "mouseup",
	pointerenter: "mouseenter",
	pointerdown: "mousedown",
	pointermove: "mousemove",
	pointerup: "mouseup",
	pointerleave: "mouseout",
	pointerout: "mouseout"
}, af = (e) => e === null || e === "";
function of(e, t) {
	let n = e.style, r = e.getAttribute("height"), i = e.getAttribute("width");
	if (e[nf] = { initial: {
		height: r,
		width: i,
		style: {
			display: n.display,
			height: n.height,
			width: n.width
		}
	} }, n.display = n.display || "block", n.boxSizing = n.boxSizing || "border-box", af(i)) {
		let t = pu(e, "width");
		t !== void 0 && (e.width = t);
	}
	if (af(r)) if (e.style.height === "") e.height = e.width / (t || 2);
	else {
		let t = pu(e, "height");
		t !== void 0 && (e.height = t);
	}
	return e;
}
var sf = fu ? { passive: !0 } : !1;
function cf(e, t, n) {
	e && e.addEventListener(t, n, sf);
}
function lf(e, t, n) {
	e && e.canvas && e.canvas.removeEventListener(t, n, sf);
}
function uf(e, t) {
	let n = rf[e.type] || e.type, { x: r, y: i } = su(e, t);
	return {
		type: n,
		chart: t,
		native: e,
		x: r === void 0 ? null : r,
		y: i === void 0 ? null : i
	};
}
function df(e, t) {
	for (let n of e) if (n === t || n.contains(t)) return !0;
}
function ff(e, t, n) {
	let r = e.canvas, i = new MutationObserver((e) => {
		let t = !1;
		for (let n of e) t ||= df(n.addedNodes, r), t &&= !df(n.removedNodes, r);
		t && n();
	});
	return i.observe(document, {
		childList: !0,
		subtree: !0
	}), i;
}
function pf(e, t, n) {
	let r = e.canvas, i = new MutationObserver((e) => {
		let t = !1;
		for (let n of e) t ||= df(n.removedNodes, r), t &&= !df(n.addedNodes, r);
		t && n();
	});
	return i.observe(document, {
		childList: !0,
		subtree: !0
	}), i;
}
var mf = /* @__PURE__ */ new Map(), hf = 0;
function gf() {
	let e = window.devicePixelRatio;
	e !== hf && (hf = e, mf.forEach((t, n) => {
		n.currentDevicePixelRatio !== e && t();
	}));
}
function _f(e, t) {
	mf.size || window.addEventListener("resize", gf), mf.set(e, t);
}
function vf(e) {
	mf.delete(e), mf.size || window.removeEventListener("resize", gf);
}
function yf(e, t, n) {
	let r = e.canvas, i = r && $l(r);
	if (!i) return;
	let a = Sc((e, t) => {
		let r = i.clientWidth;
		n(e, t), r < i.clientWidth && n();
	}, window), o = new ResizeObserver((e) => {
		let t = e[0], n = t.contentRect.width, r = t.contentRect.height;
		n === 0 && r === 0 || a(n, r);
	});
	return o.observe(i), _f(e, a), o;
}
function bf(e, t, n) {
	n && n.disconnect(), t === "resize" && vf(e);
}
function xf(e, t, n) {
	let r = e.canvas, i = Sc((t) => {
		e.ctx !== null && n(uf(t, e));
	}, e);
	return cf(r, t, i), i;
}
var Sf = class extends ef {
	acquireContext(e, t) {
		let n = e && e.getContext && e.getContext("2d");
		return n && n.canvas === e ? (of(e, t), n) : null;
	}
	releaseContext(e) {
		let t = e.canvas;
		if (!t[nf]) return !1;
		let n = t[nf].initial;
		["height", "width"].forEach((e) => {
			let r = n[e];
			L(r) ? t.removeAttribute(e) : t.setAttribute(e, r);
		});
		let r = n.style || {};
		return Object.keys(r).forEach((e) => {
			t.style[e] = r[e];
		}), t.width = t.width, delete t[nf], !0;
	}
	addEventListener(e, t, n) {
		this.removeEventListener(e, t);
		let r = e.$proxies ||= {};
		r[t] = ({
			attach: ff,
			detach: pf,
			resize: yf
		}[t] || xf)(e, t, n);
	}
	removeEventListener(e, t) {
		let n = e.$proxies ||= {}, r = n[t];
		r && (({
			attach: bf,
			detach: bf,
			resize: bf
		}[t] || lf)(e, t, r), n[t] = void 0);
	}
	getDevicePixelRatio() {
		return window.devicePixelRatio;
	}
	getMaximumSize(e, t, n, r) {
		return uu(e, t, n, r);
	}
	isAttached(e) {
		let t = e && $l(e);
		return !!(t && t.isConnected);
	}
};
function Cf(e) {
	return !Ql() || typeof OffscreenCanvas < "u" && e instanceof OffscreenCanvas ? tf : Sf;
}
var wf = class {
	static defaults = {};
	static defaultRoutes = void 0;
	x;
	y;
	active = !1;
	options;
	$animations;
	tooltipPosition(e) {
		let { x: t, y: n } = this.getProps(["x", "y"], e);
		return {
			x: t,
			y: n
		};
	}
	hasValue() {
		return $s(this.x) && $s(this.y);
	}
	getProps(e, t) {
		let n = this.$animations;
		if (!t || !n) return this;
		let r = {};
		return e.forEach((e) => {
			r[e] = n[e] && n[e].active() ? n[e]._to : this[e];
		}), r;
	}
};
function Tf(e, t) {
	let n = e.options.ticks, r = Ef(e), i = Math.min(n.maxTicksLimit || r, r), a = n.major.enabled ? Of(t) : [], o = a.length, s = a[0], c = a[o - 1], l = [];
	if (o > i) return kf(t, l, a, o / i), l;
	let u = Df(a, t, i);
	if (o > 0) {
		let e, n, r = o > 1 ? Math.round((c - s) / (o - 1)) : null;
		for (Af(t, l, u, L(r) ? 0 : s - r, s), e = 0, n = o - 1; e < n; e++) Af(t, l, u, a[e], a[e + 1]);
		return Af(t, l, u, c, L(r) ? t.length : c + r), l;
	}
	return Af(t, l, u), l;
}
function Ef(e) {
	let t = e.options.offset, n = e._tickSize(), r = e._length / n + +!t, i = e._maxLength / n;
	return Math.floor(Math.min(r, i));
}
function Df(e, t, n) {
	let r = jf(e), i = t.length / n;
	if (!r) return Math.max(i, 1);
	let a = Zs(r);
	for (let e = 0, t = a.length - 1; e < t; e++) {
		let t = a[e];
		if (t > i) return t;
	}
	return Math.max(i, 1);
}
function Of(e) {
	let t = [], n, r;
	for (n = 0, r = e.length; n < r; n++) e[n].major && t.push(n);
	return t;
}
function kf(e, t, n, r) {
	let i = 0, a = n[0], o;
	for (r = Math.ceil(r), o = 0; o < e.length; o++) o === a && (t.push(e[o]), i++, a = n[i * r]);
}
function Af(e, t, n, r, i) {
	let a = V(r, 0), o = Math.min(V(i, e.length), e.length), s = 0, c, l, u;
	for (n = Math.ceil(n), i && (c = i - r, n = c / Math.floor(c / n)), u = a; u < 0;) s++, u = Math.round(a + s * n);
	for (l = Math.max(a, 0); l < o; l++) l === u && (t.push(e[l]), s++, u = Math.round(a + s * n));
}
function jf(e) {
	let t = e.length, n, r;
	if (t < 2) return !1;
	for (r = e[0], n = 1; n < t; ++n) if (e[n] - e[n - 1] !== r) return !1;
	return r;
}
var Mf = (e) => e === "left" ? "right" : e === "right" ? "left" : e, Nf = (e, t, n) => t === "top" || t === "left" ? e[t] + n : e[t] - n, Pf = (e, t) => Math.min(t || e, e);
function Ff(e, t) {
	let n = [], r = e.length / t, i = e.length, a = 0;
	for (; a < i; a += r) n.push(e[Math.floor(a)]);
	return n;
}
function If(e, t, n) {
	let r = e.ticks.length, i = Math.min(t, r - 1), a = e._startPixel, o = e._endPixel, s = 1e-6, c = e.getPixelForTick(i), l;
	if (!(n && (l = r === 1 ? Math.max(c - a, o - c) : t === 0 ? (e.getPixelForTick(1) - c) / 2 : (c - e.getPixelForTick(i - 1)) / 2, c += i < t ? l : -l, c < a - s || c > o + s))) return c;
}
function Lf(e, t) {
	U(e, (e) => {
		let n = e.gc, r = n.length / 2, i;
		if (r > t) {
			for (i = 0; i < r; ++i) delete e.data[n[i]];
			n.splice(0, r);
		}
	});
}
function Rf(e) {
	return e.drawTicks ? e.tickLength : 0;
}
function zf(e, t) {
	if (!e.display) return 0;
	let n = yl(e.font, t), r = vl(e.padding);
	return (R(e.text) ? e.text.length : 1) * n.lineHeight + r.height;
}
function Bf(e, t) {
	return Sl(e, {
		scale: t,
		type: "scale"
	});
}
function Vf(e, t, n) {
	return Sl(e, {
		tick: n,
		index: t,
		type: "tick"
	});
}
function Hf(e, t, n) {
	let r = wc(e);
	return (n && t !== "right" || !n && t === "right") && (r = Mf(r)), r;
}
function Uf(e, t, n, r) {
	let { top: i, left: a, bottom: o, right: s, chart: c } = e, { chartArea: l, scales: u } = c, d = 0, f, p, m, h = o - i, g = s - a;
	if (e.isHorizontal()) {
		if (p = Tc(r, a, s), z(n)) {
			let e = Object.keys(n)[0], r = n[e];
			m = u[e].getPixelForValue(r) + h - t;
		} else m = n === "center" ? (l.bottom + l.top) / 2 + h - t : Nf(e, n, t);
		f = s - a;
	} else {
		if (z(n)) {
			let e = Object.keys(n)[0], r = n[e];
			p = u[e].getPixelForValue(r) - g + t;
		} else p = n === "center" ? (l.left + l.right) / 2 - g + t : Nf(e, n, t);
		m = Tc(r, o, i), d = n === "left" ? -Ws : Ws;
	}
	return {
		titleX: p,
		titleY: m,
		maxWidth: f,
		rotation: d
	};
}
var Wf = class e extends wf {
	constructor(e) {
		super(), this.id = e.id, this.type = e.type, this.options = void 0, this.ctx = e.ctx, this.chart = e.chart, this.top = void 0, this.bottom = void 0, this.left = void 0, this.right = void 0, this.width = void 0, this.height = void 0, this._margins = {
			left: 0,
			right: 0,
			top: 0,
			bottom: 0
		}, this.maxWidth = void 0, this.maxHeight = void 0, this.paddingTop = void 0, this.paddingBottom = void 0, this.paddingLeft = void 0, this.paddingRight = void 0, this.axis = void 0, this.labelRotation = void 0, this.min = void 0, this.max = void 0, this._range = void 0, this.ticks = [], this._gridLineItems = null, this._labelItems = null, this._labelSizes = null, this._length = 0, this._maxLength = 0, this._longestTextCache = {}, this._startPixel = void 0, this._endPixel = void 0, this._reversePixels = !1, this._userMax = void 0, this._userMin = void 0, this._suggestedMax = void 0, this._suggestedMin = void 0, this._ticksLength = 0, this._borderValue = 0, this._cache = {}, this._dataLimitsCached = !1, this.$context = void 0;
	}
	init(e) {
		this.options = e.setContext(this.getContext()), this.axis = e.axis, this._userMin = this.parse(e.min), this._userMax = this.parse(e.max), this._suggestedMin = this.parse(e.suggestedMin), this._suggestedMax = this.parse(e.suggestedMax);
	}
	parse(e, t) {
		return e;
	}
	getUserBounds() {
		let { _userMin: e, _userMax: t, _suggestedMin: n, _suggestedMax: r } = this;
		return e = Ss(e, Infinity), t = Ss(t, -Infinity), n = Ss(n, Infinity), r = Ss(r, -Infinity), {
			min: Ss(e, n),
			max: Ss(t, r),
			minDefined: B(e),
			maxDefined: B(t)
		};
	}
	getMinMax(e) {
		let { min: t, max: n, minDefined: r, maxDefined: i } = this.getUserBounds(), a;
		if (r && i) return {
			min: t,
			max: n
		};
		let o = this.getMatchingVisibleMetas();
		for (let s = 0, c = o.length; s < c; ++s) a = o[s].controller.getMinMax(this, e), r || (t = Math.min(t, a.min)), i || (n = Math.max(n, a.max));
		return t = i && t > n ? n : t, n = r && t > n ? t : n, {
			min: Ss(t, Ss(n, t)),
			max: Ss(n, Ss(t, n))
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
		let e = this.chart.data;
		return this.options.labels || (this.isHorizontal() ? e.xLabels : e.yLabels) || e.labels || [];
	}
	getLabelItems(e = this.chart.chartArea) {
		return this._labelItems ||= this._computeLabelItems(e);
	}
	beforeLayout() {
		this._cache = {}, this._dataLimitsCached = !1;
	}
	beforeUpdate() {
		H(this.options.beforeUpdate, [this]);
	}
	update(e, t, n) {
		let { beginAtZero: r, grace: i, ticks: a } = this.options, o = a.sampleSize;
		this.beforeUpdate(), this.maxWidth = e, this.maxHeight = t, this._margins = n = Object.assign({
			left: 0,
			right: 0,
			top: 0,
			bottom: 0
		}, n), this.ticks = null, this._labelSizes = null, this._gridLineItems = null, this._labelItems = null, this.beforeSetDimensions(), this.setDimensions(), this.afterSetDimensions(), this._maxLength = this.isHorizontal() ? this.width + n.left + n.right : this.height + n.top + n.bottom, this._dataLimitsCached ||= (this.beforeDataLimits(), this.determineDataLimits(), this.afterDataLimits(), this._range = xl(this, i, r), !0), this.beforeBuildTicks(), this.ticks = this.buildTicks() || [], this.afterBuildTicks();
		let s = o < this.ticks.length;
		this._convertTicksToLabels(s ? Ff(this.ticks, o) : this.ticks), this.configure(), this.beforeCalculateLabelRotation(), this.calculateLabelRotation(), this.afterCalculateLabelRotation(), a.display && (a.autoSkip || a.source === "auto") && (this.ticks = Tf(this, this.ticks), this._labelSizes = null, this.afterAutoSkip()), s && this._convertTicksToLabels(this.ticks), this.beforeFit(), this.fit(), this.afterFit(), this.afterUpdate();
	}
	configure() {
		let e = this.options.reverse, t, n;
		this.isHorizontal() ? (t = this.left, n = this.right) : (t = this.top, n = this.bottom, e = !e), this._startPixel = t, this._endPixel = n, this._reversePixels = e, this._length = n - t, this._alignToPixels = this.options.alignToPixels;
	}
	afterUpdate() {
		H(this.options.afterUpdate, [this]);
	}
	beforeSetDimensions() {
		H(this.options.beforeSetDimensions, [this]);
	}
	setDimensions() {
		this.isHorizontal() ? (this.width = this.maxWidth, this.left = 0, this.right = this.width) : (this.height = this.maxHeight, this.top = 0, this.bottom = this.height), this.paddingLeft = 0, this.paddingTop = 0, this.paddingRight = 0, this.paddingBottom = 0;
	}
	afterSetDimensions() {
		H(this.options.afterSetDimensions, [this]);
	}
	_callHooks(e) {
		this.chart.notifyPlugins(e, this.getContext()), H(this.options[e], [this]);
	}
	beforeDataLimits() {
		this._callHooks("beforeDataLimits");
	}
	determineDataLimits() {}
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
		H(this.options.beforeTickToLabelConversion, [this]);
	}
	generateTickLabels(e) {
		let t = this.options.ticks, n, r, i;
		for (n = 0, r = e.length; n < r; n++) i = e[n], i.label = H(t.callback, [
			i.value,
			n,
			e
		], this);
	}
	afterTickToLabelConversion() {
		H(this.options.afterTickToLabelConversion, [this]);
	}
	beforeCalculateLabelRotation() {
		H(this.options.beforeCalculateLabelRotation, [this]);
	}
	calculateLabelRotation() {
		let e = this.options, t = e.ticks, n = Pf(this.ticks.length, e.ticks.maxTicksLimit), r = t.minRotation || 0, i = t.maxRotation, a = r, o, s, c;
		if (!this._isVisible() || !t.display || r >= i || n <= 1 || !this.isHorizontal()) {
			this.labelRotation = r;
			return;
		}
		let l = this._getLabelSizes(), u = l.widest.width, d = l.highest.height, f = uc(this.chart.width - u, 0, this.maxWidth);
		o = e.offset ? this.maxWidth / n : f / (n - 1), u + 6 > o && (o = f / (n - (e.offset ? .5 : 1)), s = this.maxHeight - Rf(e.grid) - t.padding - zf(e.title, this.chart.options.font), c = Math.sqrt(u * u + d * d), a = rc(Math.min(Math.asin(uc((l.highest.height + 6) / o, -1, 1)), Math.asin(uc(s / c, -1, 1)) - Math.asin(uc(d / c, -1, 1)))), a = Math.max(r, Math.min(i, a))), this.labelRotation = a;
	}
	afterCalculateLabelRotation() {
		H(this.options.afterCalculateLabelRotation, [this]);
	}
	afterAutoSkip() {}
	beforeFit() {
		H(this.options.beforeFit, [this]);
	}
	fit() {
		let e = {
			width: 0,
			height: 0
		}, { chart: t, options: { ticks: n, title: r, grid: i } } = this, a = this._isVisible(), o = this.isHorizontal();
		if (a) {
			let a = zf(r, t.options.font);
			if (o ? (e.width = this.maxWidth, e.height = Rf(i) + a) : (e.height = this.maxHeight, e.width = Rf(i) + a), n.display && this.ticks.length) {
				let { first: t, last: r, widest: i, highest: a } = this._getLabelSizes(), s = n.padding * 2, c = nc(this.labelRotation), l = Math.cos(c), u = Math.sin(c);
				if (o) {
					let t = n.mirror ? 0 : u * i.width + l * a.height;
					e.height = Math.min(this.maxHeight, e.height + t + s);
				} else {
					let t = n.mirror ? 0 : l * i.width + u * a.height;
					e.width = Math.min(this.maxWidth, e.width + t + s);
				}
				this._calculatePadding(t, r, u, l);
			}
		}
		this._handleMargins(), o ? (this.width = this._length = t.width - this._margins.left - this._margins.right, this.height = e.height) : (this.width = e.width, this.height = this._length = t.height - this._margins.top - this._margins.bottom);
	}
	_calculatePadding(e, t, n, r) {
		let { ticks: { align: i, padding: a }, position: o } = this.options, s = this.labelRotation !== 0, c = o !== "top" && this.axis === "x";
		if (this.isHorizontal()) {
			let o = this.getPixelForTick(0) - this.left, l = this.right - this.getPixelForTick(this.ticks.length - 1), u = 0, d = 0;
			s ? c ? (u = r * e.width, d = n * t.height) : (u = n * e.height, d = r * t.width) : i === "start" ? d = t.width : i === "end" ? u = e.width : i !== "inner" && (u = e.width / 2, d = t.width / 2), this.paddingLeft = Math.max((u - o + a) * this.width / (this.width - o), 0), this.paddingRight = Math.max((d - l + a) * this.width / (this.width - l), 0);
		} else {
			let n = t.height / 2, r = e.height / 2;
			i === "start" ? (n = 0, r = e.height) : i === "end" && (n = t.height, r = 0), this.paddingTop = n + a, this.paddingBottom = r + a;
		}
	}
	_handleMargins() {
		this._margins && (this._margins.left = Math.max(this.paddingLeft, this._margins.left), this._margins.top = Math.max(this.paddingTop, this._margins.top), this._margins.right = Math.max(this.paddingRight, this._margins.right), this._margins.bottom = Math.max(this.paddingBottom, this._margins.bottom));
	}
	afterFit() {
		H(this.options.afterFit, [this]);
	}
	isHorizontal() {
		let { axis: e, position: t } = this.options;
		return t === "top" || t === "bottom" || e === "x";
	}
	isFullSize() {
		return this.options.fullSize;
	}
	_convertTicksToLabels(e) {
		this.beforeTickToLabelConversion(), this.generateTickLabels(e);
		let t, n;
		for (t = 0, n = e.length; t < n; t++) L(e[t].label) && (e.splice(t, 1), n--, t--);
		this.afterTickToLabelConversion();
	}
	_getLabelSizes() {
		let e = this._labelSizes;
		if (!e) {
			let t = this.options.ticks.sampleSize, n = this.ticks;
			t < n.length && (n = Ff(n, t)), this._labelSizes = e = this._computeLabelSizes(n, n.length, this.options.ticks.maxTicksLimit);
		}
		return e;
	}
	_computeLabelSizes(e, t, n) {
		let { ctx: r, _longestTextCache: i } = this, a = [], o = [], s = Math.floor(t / Pf(t, n)), c = 0, l = 0, u, d, f, p, m, h, g, _, v, y, b;
		for (u = 0; u < t; u += s) {
			if (p = e[u].label, m = this._resolveTickFontOptions(u), r.font = h = m.string, g = i[h] = i[h] || {
				data: {},
				gc: []
			}, _ = m.lineHeight, v = y = 0, !L(p) && !R(p)) v = Yc(r, g.data, g.gc, v, p), y = _;
			else if (R(p)) for (d = 0, f = p.length; d < f; ++d) b = p[d], !L(b) && !R(b) && (v = Yc(r, g.data, g.gc, v, b), y += _);
			a.push(v), o.push(y), c = Math.max(v, c), l = Math.max(y, l);
		}
		Lf(i, t);
		let x = a.indexOf(c), S = o.indexOf(l), C = (e) => ({
			width: a[e] || 0,
			height: o[e] || 0
		});
		return {
			first: C(0),
			last: C(t - 1),
			widest: C(x),
			highest: C(S),
			widths: a,
			heights: o
		};
	}
	getLabelForValue(e) {
		return e;
	}
	getPixelForValue(e, t) {
		return NaN;
	}
	getValueForPixel(e) {}
	getPixelForTick(e) {
		let t = this.ticks;
		return e < 0 || e > t.length - 1 ? null : this.getPixelForValue(t[e].value);
	}
	getPixelForDecimal(e) {
		this._reversePixels && (e = 1 - e);
		let t = this._startPixel + e * this._length;
		return dc(this._alignToPixels ? Zc(this.chart, t, 0) : t);
	}
	getDecimalForPixel(e) {
		let t = (e - this._startPixel) / this._length;
		return this._reversePixels ? 1 - t : t;
	}
	getBasePixel() {
		return this.getPixelForValue(this.getBaseValue());
	}
	getBaseValue() {
		let { min: e, max: t } = this;
		return e < 0 && t < 0 ? t : e > 0 && t > 0 ? e : 0;
	}
	getContext(e) {
		let t = this.ticks || [];
		if (e >= 0 && e < t.length) {
			let n = t[e];
			return n.$context ||= Vf(this.getContext(), e, n);
		}
		return this.$context ||= Bf(this.chart.getContext(), this);
	}
	_tickSize() {
		let e = this.options.ticks, t = nc(this.labelRotation), n = Math.abs(Math.cos(t)), r = Math.abs(Math.sin(t)), i = this._getLabelSizes(), a = e.autoSkipPadding || 0, o = i ? i.widest.width + a : 0, s = i ? i.highest.height + a : 0;
		return this.isHorizontal() ? s * n > o * r ? o / n : s / r : s * r < o * n ? s / n : o / r;
	}
	_isVisible() {
		let e = this.options.display;
		return e === "auto" ? this.getMatchingVisibleMetas().length > 0 : !!e;
	}
	_computeGridLineItems(e) {
		let t = this.axis, n = this.chart, r = this.options, { grid: i, position: a, border: o } = r, s = i.offset, c = this.isHorizontal(), l = this.ticks.length + +!!s, u = Rf(i), d = [], f = o.setContext(this.getContext()), p = f.display ? f.width : 0, m = p / 2, h = function(e) {
			return Zc(n, e, p);
		}, g, _, v, y, b, x, S, C, w, T, E, D;
		if (a === "top") g = h(this.bottom), x = this.bottom - u, C = g - m, T = h(e.top) + m, D = e.bottom;
		else if (a === "bottom") g = h(this.top), T = e.top, D = h(e.bottom) - m, x = g + m, C = this.top + u;
		else if (a === "left") g = h(this.right), b = this.right - u, S = g - m, w = h(e.left) + m, E = e.right;
		else if (a === "right") g = h(this.left), w = e.left, E = h(e.right) - m, b = g + m, S = this.left + u;
		else if (t === "x") {
			if (a === "center") g = h((e.top + e.bottom) / 2 + .5);
			else if (z(a)) {
				let e = Object.keys(a)[0], t = a[e];
				g = h(this.chart.scales[e].getPixelForValue(t));
			}
			T = e.top, D = e.bottom, x = g + m, C = x + u;
		} else if (t === "y") {
			if (a === "center") g = h((e.left + e.right) / 2);
			else if (z(a)) {
				let e = Object.keys(a)[0], t = a[e];
				g = h(this.chart.scales[e].getPixelForValue(t));
			}
			b = g - m, S = b - u, w = e.left, E = e.right;
		}
		let O = V(r.ticks.maxTicksLimit, l), ee = Math.max(1, Math.ceil(l / O));
		for (_ = 0; _ < l; _ += ee) {
			let e = this.getContext(_), t = i.setContext(e), r = o.setContext(e), a = t.lineWidth, l = t.color, u = r.dash || [], f = r.dashOffset, p = t.tickWidth, m = t.tickColor, h = t.tickBorderDash || [], g = t.tickBorderDashOffset;
			v = If(this, _, s), v !== void 0 && (y = Zc(n, v, a), c ? b = S = w = E = y : x = C = T = D = y, d.push({
				tx1: b,
				ty1: x,
				tx2: S,
				ty2: C,
				x1: w,
				y1: T,
				x2: E,
				y2: D,
				width: a,
				color: l,
				borderDash: u,
				borderDashOffset: f,
				tickWidth: p,
				tickColor: m,
				tickBorderDash: h,
				tickBorderDashOffset: g
			}));
		}
		return this._ticksLength = l, this._borderValue = g, d;
	}
	_computeLabelItems(e) {
		let t = this.axis, n = this.options, { position: r, ticks: i } = n, a = this.isHorizontal(), o = this.ticks, { align: s, crossAlign: c, padding: l, mirror: u } = i, d = Rf(n.grid), f = d + l, p = u ? -l : f, m = -nc(this.labelRotation), h = [], g, _, v, y, b, x, S, C, w, T, E, D, O = "middle";
		if (r === "top") x = this.bottom - p, S = this._getXAxisLabelAlignment();
		else if (r === "bottom") x = this.top + p, S = this._getXAxisLabelAlignment();
		else if (r === "left") {
			let e = this._getYAxisLabelAlignment(d);
			S = e.textAlign, b = e.x;
		} else if (r === "right") {
			let e = this._getYAxisLabelAlignment(d);
			S = e.textAlign, b = e.x;
		} else if (t === "x") {
			if (r === "center") x = (e.top + e.bottom) / 2 + f;
			else if (z(r)) {
				let e = Object.keys(r)[0], t = r[e];
				x = this.chart.scales[e].getPixelForValue(t) + f;
			}
			S = this._getXAxisLabelAlignment();
		} else if (t === "y") {
			if (r === "center") b = (e.left + e.right) / 2 - f;
			else if (z(r)) {
				let e = Object.keys(r)[0], t = r[e];
				b = this.chart.scales[e].getPixelForValue(t);
			}
			S = this._getYAxisLabelAlignment(d).textAlign;
		}
		t === "y" && (s === "start" ? O = "top" : s === "end" && (O = "bottom"));
		let ee = this._getLabelSizes();
		for (g = 0, _ = o.length; g < _; ++g) {
			v = o[g], y = v.label;
			let e = i.setContext(this.getContext(g));
			C = this.getPixelForTick(g) + i.labelOffset, w = this._resolveTickFontOptions(g), T = w.lineHeight, E = R(y) ? y.length : 1;
			let t = E / 2, n = e.color, s = e.textStrokeColor, l = e.textStrokeWidth, d = S;
			a ? (b = C, S === "inner" && (d = g === _ - 1 ? this.options.reverse ? "left" : "right" : g === 0 ? this.options.reverse ? "right" : "left" : "center"), D = r === "top" ? c === "near" || m !== 0 ? -E * T + T / 2 : c === "center" ? -ee.highest.height / 2 - t * T + T : -ee.highest.height + T / 2 : c === "near" || m !== 0 ? T / 2 : c === "center" ? ee.highest.height / 2 - t * T : ee.highest.height - E * T, u && (D *= -1), m !== 0 && !e.showLabelBackdrop && (b += T / 2 * Math.sin(m))) : (x = C, D = (1 - E) * T / 2);
			let f;
			if (e.showLabelBackdrop) {
				let t = vl(e.backdropPadding), n = ee.heights[g], r = ee.widths[g], i = D - t.top, a = 0 - t.left;
				switch (O) {
					case "middle":
						i -= n / 2;
						break;
					case "bottom":
						i -= n;
						break;
				}
				switch (S) {
					case "center":
						a -= r / 2;
						break;
					case "right":
						a -= r;
						break;
					case "inner":
						g === _ - 1 ? a -= r : g > 0 && (a -= r / 2);
						break;
				}
				f = {
					left: a,
					top: i,
					width: r + t.width,
					height: n + t.height,
					color: e.backdropColor
				};
			}
			h.push({
				label: y,
				font: w,
				textOffset: D,
				options: {
					rotation: m,
					color: n,
					strokeColor: s,
					strokeWidth: l,
					textAlign: d,
					textBaseline: O,
					translation: [b, x],
					backdrop: f
				}
			});
		}
		return h;
	}
	_getXAxisLabelAlignment() {
		let { position: e, ticks: t } = this.options;
		if (-nc(this.labelRotation)) return e === "top" ? "left" : "right";
		let n = "center";
		return t.align === "start" ? n = "left" : t.align === "end" ? n = "right" : t.align === "inner" && (n = "inner"), n;
	}
	_getYAxisLabelAlignment(e) {
		let { position: t, ticks: { crossAlign: n, mirror: r, padding: i } } = this.options, a = this._getLabelSizes(), o = e + i, s = a.widest.width, c, l;
		return t === "left" ? r ? (l = this.right + i, n === "near" ? c = "left" : n === "center" ? (c = "center", l += s / 2) : (c = "right", l += s)) : (l = this.right - o, n === "near" ? c = "right" : n === "center" ? (c = "center", l -= s / 2) : (c = "left", l = this.left)) : t === "right" ? r ? (l = this.left + i, n === "near" ? c = "right" : n === "center" ? (c = "center", l -= s / 2) : (c = "left", l -= s)) : (l = this.left + o, n === "near" ? c = "left" : n === "center" ? (c = "center", l += s / 2) : (c = "right", l = this.right)) : c = "right", {
			textAlign: c,
			x: l
		};
	}
	_computeLabelArea() {
		if (this.options.ticks.mirror) return;
		let e = this.chart, t = this.options.position;
		if (t === "left" || t === "right") return {
			top: 0,
			left: this.left,
			bottom: e.height,
			right: this.right
		};
		if (t === "top" || t === "bottom") return {
			top: this.top,
			left: 0,
			bottom: this.bottom,
			right: e.width
		};
	}
	drawBackground() {
		let { ctx: e, options: { backgroundColor: t }, left: n, top: r, width: i, height: a } = this;
		t && (e.save(), e.fillStyle = t, e.fillRect(n, r, i, a), e.restore());
	}
	getLineWidthForValue(e) {
		let t = this.options.grid;
		if (!this._isVisible() || !t.display) return 0;
		let n = this.ticks.findIndex((t) => t.value === e);
		return n >= 0 ? t.setContext(this.getContext(n)).lineWidth : 0;
	}
	drawGrid(e) {
		let t = this.options.grid, n = this.ctx, r = this._gridLineItems ||= this._computeGridLineItems(e), i, a, o = (e, t, r) => {
			!r.width || !r.color || (n.save(), n.lineWidth = r.width, n.strokeStyle = r.color, n.setLineDash(r.borderDash || []), n.lineDashOffset = r.borderDashOffset, n.beginPath(), n.moveTo(e.x, e.y), n.lineTo(t.x, t.y), n.stroke(), n.restore());
		};
		if (t.display) for (i = 0, a = r.length; i < a; ++i) {
			let e = r[i];
			t.drawOnChartArea && o({
				x: e.x1,
				y: e.y1
			}, {
				x: e.x2,
				y: e.y2
			}, e), t.drawTicks && o({
				x: e.tx1,
				y: e.ty1
			}, {
				x: e.tx2,
				y: e.ty2
			}, {
				color: e.tickColor,
				width: e.tickWidth,
				borderDash: e.tickBorderDash,
				borderDashOffset: e.tickBorderDashOffset
			});
		}
	}
	drawBorder() {
		let { chart: e, ctx: t, options: { border: n, grid: r } } = this, i = n.setContext(this.getContext()), a = n.display ? i.width : 0;
		if (!a) return;
		let o = r.setContext(this.getContext(0)).lineWidth, s = this._borderValue, c, l, u, d;
		this.isHorizontal() ? (c = Zc(e, this.left, a) - a / 2, l = Zc(e, this.right, o) + o / 2, u = d = s) : (u = Zc(e, this.top, a) - a / 2, d = Zc(e, this.bottom, o) + o / 2, c = l = s), t.save(), t.lineWidth = i.width, t.strokeStyle = i.color, t.beginPath(), t.moveTo(c, u), t.lineTo(l, d), t.stroke(), t.restore();
	}
	drawLabels(e) {
		if (!this.options.ticks.display) return;
		let t = this.ctx, n = this._computeLabelArea();
		n && nl(t, n);
		let r = this.getLabelItems(e);
		for (let e of r) {
			let n = e.options, r = e.font, i = e.label, a = e.textOffset;
			ll(t, i, 0, a, r, n);
		}
		n && rl(t);
	}
	drawTitle() {
		let { ctx: e, options: { position: t, title: n, reverse: r } } = this;
		if (!n.display) return;
		let i = yl(n.font), a = vl(n.padding), o = n.align, s = i.lineHeight / 2;
		t === "bottom" || t === "center" || z(t) ? (s += a.bottom, R(n.text) && (s += i.lineHeight * (n.text.length - 1))) : s += a.top;
		let { titleX: c, titleY: l, maxWidth: u, rotation: d } = Uf(this, s, t, o);
		ll(e, n.text, 0, 0, i, {
			color: n.color,
			maxWidth: u,
			rotation: d,
			textAlign: Hf(o, t, r),
			textBaseline: "middle",
			translation: [c, l]
		});
	}
	draw(e) {
		this._isVisible() && (this.drawBackground(), this.drawGrid(e), this.drawBorder(), this.drawTitle(), this.drawLabels(e));
	}
	_layers() {
		let t = this.options, n = t.ticks && t.ticks.z || 0, r = V(t.grid && t.grid.z, -1), i = V(t.border && t.border.z, 0);
		return !this._isVisible() || this.draw !== e.prototype.draw ? [{
			z: n,
			draw: (e) => {
				this.draw(e);
			}
		}] : [
			{
				z: r,
				draw: (e) => {
					this.drawBackground(), this.drawGrid(e), this.drawTitle();
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
				draw: (e) => {
					this.drawLabels(e);
				}
			}
		];
	}
	getMatchingVisibleMetas(e) {
		let t = this.chart.getSortedVisibleDatasetMetas(), n = this.axis + "AxisID", r = [], i, a;
		for (i = 0, a = t.length; i < a; ++i) {
			let a = t[i];
			a[n] === this.id && (!e || a.type === e) && r.push(a);
		}
		return r;
	}
	_resolveTickFontOptions(e) {
		return yl(this.options.ticks.setContext(this.getContext(e)).font);
	}
	_maxDigits() {
		let e = this._resolveTickFontOptions(0).lineHeight;
		return (this.isHorizontal() ? this.width : this.height) / e;
	}
}, Gf = class {
	constructor(e, t, n) {
		this.type = e, this.scope = t, this.override = n, this.items = Object.create(null);
	}
	isForType(e) {
		return Object.prototype.isPrototypeOf.call(this.type.prototype, e.prototype);
	}
	register(e) {
		let t = Object.getPrototypeOf(e), n;
		Jf(t) && (n = this.register(t));
		let r = this.items, i = e.id, a = this.scope + "." + i;
		if (!i) throw Error("class does not have id: " + e);
		return i in r ? a : (r[i] = e, Kf(e, a, n), this.override && G.override(e.id, e.overrides), a);
	}
	get(e) {
		return this.items[e];
	}
	unregister(e) {
		let t = this.items, n = e.id, r = this.scope;
		n in t && delete t[n], r && n in G[r] && (delete G[r][n], this.override && delete Wc[n]);
	}
};
function Kf(e, t, n) {
	let r = Os(Object.create(null), [
		n ? G.get(n) : {},
		G.get(t),
		e.defaults
	]);
	G.set(t, r), e.defaultRoutes && qf(t, e.defaultRoutes), e.descriptors && G.describe(t, e.descriptors);
}
function qf(e, t) {
	Object.keys(t).forEach((n) => {
		let r = n.split("."), i = r.pop(), a = [e].concat(r).join("."), o = t[n].split("."), s = o.pop(), c = o.join(".");
		G.route(a, i, c, s);
	});
}
function Jf(e) {
	return "id" in e && "defaults" in e;
}
var Yf = /* #__PURE__ */ new class {
	constructor() {
		this.controllers = new Gf(ld, "datasets", !0), this.elements = new Gf(wf, "elements"), this.plugins = new Gf(Object, "plugins"), this.scales = new Gf(Wf, "scales"), this._typedRegistries = [
			this.controllers,
			this.scales,
			this.elements
		];
	}
	add(...e) {
		this._each("register", e);
	}
	remove(...e) {
		this._each("unregister", e);
	}
	addControllers(...e) {
		this._each("register", e, this.controllers);
	}
	addElements(...e) {
		this._each("register", e, this.elements);
	}
	addPlugins(...e) {
		this._each("register", e, this.plugins);
	}
	addScales(...e) {
		this._each("register", e, this.scales);
	}
	getController(e) {
		return this._get(e, this.controllers, "controller");
	}
	getElement(e) {
		return this._get(e, this.elements, "element");
	}
	getPlugin(e) {
		return this._get(e, this.plugins, "plugin");
	}
	getScale(e) {
		return this._get(e, this.scales, "scale");
	}
	removeControllers(...e) {
		this._each("unregister", e, this.controllers);
	}
	removeElements(...e) {
		this._each("unregister", e, this.elements);
	}
	removePlugins(...e) {
		this._each("unregister", e, this.plugins);
	}
	removeScales(...e) {
		this._each("unregister", e, this.scales);
	}
	_each(e, t, n) {
		[...t].forEach((t) => {
			let r = n || this._getRegistryForType(t);
			n || r.isForType(t) || r === this.plugins && t.id ? this._exec(e, r, t) : U(t, (t) => {
				let r = n || this._getRegistryForType(t);
				this._exec(e, r, t);
			});
		});
	}
	_exec(e, t, n) {
		let r = Fs(e);
		H(n["before" + r], [], n), t[e](n), H(n["after" + r], [], n);
	}
	_getRegistryForType(e) {
		for (let t = 0; t < this._typedRegistries.length; t++) {
			let n = this._typedRegistries[t];
			if (n.isForType(e)) return n;
		}
		return this.plugins;
	}
	_get(e, t, n) {
		let r = t.get(e);
		if (r === void 0) throw Error("\"" + e + "\" is not a registered " + n + ".");
		return r;
	}
}(), Xf = class {
	constructor() {
		this._init = void 0;
	}
	notify(e, t, n, r) {
		if (t === "beforeInit" && (this._init = this._createDescriptors(e, !0), this._notify(this._init, e, "install")), this._init === void 0) return;
		let i = r ? this._descriptors(e).filter(r) : this._descriptors(e), a = this._notify(i, e, t, n);
		return t === "afterDestroy" && (this._notify(i, e, "stop"), this._notify(this._init, e, "uninstall"), this._init = void 0), a;
	}
	_notify(e, t, n, r) {
		r ||= {};
		for (let i of e) {
			let e = i.plugin, a = e[n];
			if (H(a, [
				t,
				r,
				i.options
			], e) === !1 && r.cancelable) return !1;
		}
		return !0;
	}
	invalidate() {
		L(this._cache) || (this._oldCache = this._cache, this._cache = void 0);
	}
	_descriptors(e) {
		if (this._cache) return this._cache;
		let t = this._cache = this._createDescriptors(e);
		return this._notifyStateChanges(e), t;
	}
	_createDescriptors(e, t) {
		let n = e && e.config, r = V(n.options && n.options.plugins, {}), i = Zf(n);
		return r === !1 && !t ? [] : $f(e, i, r, t);
	}
	_notifyStateChanges(e) {
		let t = this._oldCache || [], n = this._cache, r = (e, t) => e.filter((e) => !t.some((t) => e.plugin.id === t.plugin.id));
		this._notify(r(t, n), e, "stop"), this._notify(r(n, t), e, "start");
	}
};
function Zf(e) {
	let t = {}, n = [], r = Object.keys(Yf.plugins.items);
	for (let e = 0; e < r.length; e++) n.push(Yf.getPlugin(r[e]));
	let i = e.plugins || [];
	for (let e = 0; e < i.length; e++) {
		let r = i[e];
		n.indexOf(r) === -1 && (n.push(r), t[r.id] = !0);
	}
	return {
		plugins: n,
		localIds: t
	};
}
function Qf(e, t) {
	return !t && e === !1 ? null : e === !0 ? {} : e;
}
function $f(e, { plugins: t, localIds: n }, r, i) {
	let a = [], o = e.getContext();
	for (let s of t) {
		let t = s.id, c = Qf(r[t], i);
		c !== null && a.push({
			plugin: s,
			options: ep(e.config, {
				plugin: s,
				local: n[t]
			}, c, o)
		});
	}
	return a;
}
function ep(e, { plugin: t, local: n }, r, i) {
	let a = e.pluginScopeKeys(t), o = e.getOptionScopes(r, a);
	return n && t.defaults && o.push(t.defaults), e.createResolver(o, i, [""], {
		scriptable: !1,
		indexable: !1,
		allKeys: !0
	});
}
function tp(e, t) {
	let n = G.datasets[e] || {};
	return ((t.datasets || {})[e] || {}).indexAxis || t.indexAxis || n.indexAxis || "x";
}
function np(e, t) {
	let n = e;
	return e === "_index_" ? n = t : e === "_value_" && (n = t === "x" ? "y" : "x"), n;
}
function rp(e, t) {
	return e === t ? "_index_" : "_value_";
}
function ip(e) {
	if (e === "x" || e === "y" || e === "r") return e;
}
function ap(e) {
	if (e === "top" || e === "bottom") return "x";
	if (e === "left" || e === "right") return "y";
}
function op(e, ...t) {
	if (ip(e)) return e;
	for (let n of t) {
		let t = n.axis || ap(n.position) || e.length > 1 && ip(e[0].toLowerCase());
		if (t) return t;
	}
	throw Error(`Cannot determine type of '${e}' axis. Please provide 'axis' or 'position' option.`);
}
function sp(e, t, n) {
	if (n[t + "AxisID"] === e) return { axis: t };
}
function cp(e, t) {
	if (t.data && t.data.datasets) {
		let n = t.data.datasets.filter((t) => t.xAxisID === e || t.yAxisID === e);
		if (n.length) return sp(e, "x", n[0]) || sp(e, "y", n[0]);
	}
	return {};
}
function lp(e, t) {
	let n = Wc[e.type] || { scales: {} }, r = t.scales || {}, i = tp(e.type, t), a = Object.create(null);
	return Object.keys(r).forEach((t) => {
		let o = r[t];
		if (!z(o)) return console.error(`Invalid scale configuration for scale: ${t}`);
		if (o._proxy) return console.warn(`Ignoring resolver passed as options for scale: ${t}`);
		let s = op(t, o, cp(t, e), G.scales[o.type]), c = rp(s, i), l = n.scales || {};
		a[t] = ks(Object.create(null), [
			{ axis: s },
			o,
			l[s],
			l[c]
		]);
	}), e.data.datasets.forEach((n) => {
		let i = n.type || e.type, o = n.indexAxis || tp(i, t), s = (Wc[i] || {}).scales || {};
		Object.keys(s).forEach((e) => {
			let t = np(e, o), i = n[t + "AxisID"] || t;
			a[i] = a[i] || Object.create(null), ks(a[i], [
				{ axis: t },
				r[i],
				s[e]
			]);
		});
	}), Object.keys(a).forEach((e) => {
		let t = a[e];
		ks(t, [G.scales[t.type], G.scale]);
	}), a;
}
function up(e) {
	let t = e.options ||= {};
	t.plugins = V(t.plugins, {}), t.scales = lp(e, t);
}
function dp(e) {
	return e ||= {}, e.datasets = e.datasets || [], e.labels = e.labels || [], e;
}
function fp(e) {
	return e ||= {}, e.data = dp(e.data), up(e), e;
}
var pp = /* @__PURE__ */ new Map(), mp = /* @__PURE__ */ new Set();
function hp(e, t) {
	let n = pp.get(e);
	return n || (n = t(), pp.set(e, n), mp.add(n)), n;
}
var gp = (e, t, n) => {
	let r = Ps(t, n);
	r !== void 0 && e.add(r);
}, _p = class {
	constructor(e) {
		this._config = fp(e), this._scopeCache = /* @__PURE__ */ new Map(), this._resolverCache = /* @__PURE__ */ new Map();
	}
	get platform() {
		return this._config.platform;
	}
	get type() {
		return this._config.type;
	}
	set type(e) {
		this._config.type = e;
	}
	get data() {
		return this._config.data;
	}
	set data(e) {
		this._config.data = dp(e);
	}
	get options() {
		return this._config.options;
	}
	set options(e) {
		this._config.options = e;
	}
	get plugins() {
		return this._config.plugins;
	}
	update() {
		let e = this._config;
		this.clearCache(), up(e);
	}
	clearCache() {
		this._scopeCache.clear(), this._resolverCache.clear();
	}
	datasetScopeKeys(e) {
		return hp(e, () => [[`datasets.${e}`, ""]]);
	}
	datasetAnimationScopeKeys(e, t) {
		return hp(`${e}.transition.${t}`, () => [[`datasets.${e}.transitions.${t}`, `transitions.${t}`], [`datasets.${e}`, ""]]);
	}
	datasetElementScopeKeys(e, t) {
		return hp(`${e}-${t}`, () => [[
			`datasets.${e}.elements.${t}`,
			`datasets.${e}`,
			`elements.${t}`,
			""
		]]);
	}
	pluginScopeKeys(e) {
		let t = e.id, n = this.type;
		return hp(`${n}-plugin-${t}`, () => [[`plugins.${t}`, ...e.additionalOptionScopes || []]]);
	}
	_cachedScopes(e, t) {
		let n = this._scopeCache, r = n.get(e);
		return (!r || t) && (r = /* @__PURE__ */ new Map(), n.set(e, r)), r;
	}
	getOptionScopes(e, t, n) {
		let { options: r, type: i } = this, a = this._cachedScopes(e, n), o = a.get(t);
		if (o) return o;
		let s = /* @__PURE__ */ new Set();
		t.forEach((t) => {
			e && (s.add(e), t.forEach((t) => gp(s, e, t))), t.forEach((e) => gp(s, r, e)), t.forEach((e) => gp(s, Wc[i] || {}, e)), t.forEach((e) => gp(s, G, e)), t.forEach((e) => gp(s, Gc, e));
		});
		let c = Array.from(s);
		return c.length === 0 && c.push(Object.create(null)), mp.has(t) && a.set(t, c), c;
	}
	chartOptionScopes() {
		let { options: e, type: t } = this;
		return [
			e,
			Wc[t] || {},
			G.datasets[t] || {},
			{ type: t },
			G,
			Gc
		];
	}
	resolveNamedOptions(e, t, n, r = [""]) {
		let i = { $shared: !0 }, { resolver: a, subPrefixes: o } = vp(this._resolverCache, e, r), s = a;
		if (bp(a, t)) {
			i.$shared = !1, n = Ls(n) ? n() : n;
			let t = this.createResolver(e, n, o);
			s = wl(a, n, t);
		}
		for (let e of t) i[e] = s[e];
		return i;
	}
	createResolver(e, t, n = [""], r) {
		let { resolver: i } = vp(this._resolverCache, e, n);
		return z(t) ? wl(i, t, void 0, r) : i;
	}
};
function vp(e, t, n) {
	let r = e.get(t);
	r || (r = /* @__PURE__ */ new Map(), e.set(t, r));
	let i = n.join(), a = r.get(i);
	return a || (a = {
		resolver: Cl(t, n),
		subPrefixes: n.filter((e) => !e.toLowerCase().includes("hover"))
	}, r.set(i, a)), a;
}
var yp = (e) => z(e) && Object.getOwnPropertyNames(e).some((t) => Ls(e[t]));
function bp(e, t) {
	let { isScriptable: n, isIndexable: r } = Tl(e);
	for (let i of t) {
		let t = n(i), a = r(i), o = (a || t) && e[i];
		if (t && (Ls(o) || yp(o)) || a && R(o)) return !0;
	}
	return !1;
}
var xp = "4.5.1", Sp = [
	"top",
	"bottom",
	"left",
	"right",
	"chartArea"
];
function Cp(e, t) {
	return e === "top" || e === "bottom" || Sp.indexOf(e) === -1 && t === "x";
}
function wp(e, t) {
	return function(n, r) {
		return n[e] === r[e] ? n[t] - r[t] : n[e] - r[e];
	};
}
function Tp(e) {
	let t = e.chart, n = t.options.animation;
	t.notifyPlugins("afterRender"), H(n && n.onComplete, [e], t);
}
function Ep(e) {
	let t = e.chart, n = t.options.animation;
	H(n && n.onProgress, [e], t);
}
function Dp(e) {
	return Ql() && typeof e == "string" ? e = document.getElementById(e) : e && e.length && (e = e[0]), e && e.canvas && (e = e.canvas), e;
}
var Op = {}, kp = (e) => {
	let t = Dp(e);
	return Object.values(Op).filter((e) => e.canvas === t).pop();
};
function Ap(e, t, n) {
	let r = Object.keys(e);
	for (let i of r) {
		let r = +i;
		if (r >= t) {
			let a = e[i];
			delete e[i], (n > 0 || r > t) && (e[r + n] = a);
		}
	}
}
function jp(e, t, n, r) {
	return !n || e.type === "mouseout" ? null : r ? t : e;
}
var Mp = class {
	static defaults = G;
	static instances = Op;
	static overrides = Wc;
	static registry = Yf;
	static version = xp;
	static getChart = kp;
	static register(...e) {
		Yf.add(...e), Np();
	}
	static unregister(...e) {
		Yf.remove(...e), Np();
	}
	constructor(e, t) {
		let n = this.config = new _p(t), r = Dp(e), i = kp(r);
		if (i) throw Error("Canvas is already in use. Chart with ID '" + i.id + "' must be destroyed before the canvas with ID '" + i.canvas.id + "' can be reused.");
		let a = n.createResolver(n.chartOptionScopes(), this.getContext());
		this.platform = new (n.platform || (Cf(r)))(), this.platform.updateConfig(n);
		let o = this.platform.acquireContext(r, a.aspectRatio), s = o && o.canvas, c = s && s.height, l = s && s.width;
		if (this.id = xs(), this.ctx = o, this.canvas = s, this.width = l, this.height = c, this._options = a, this._aspectRatio = this.aspectRatio, this._layers = [], this._metasets = [], this._stacks = void 0, this.boxes = [], this.currentDevicePixelRatio = void 0, this.chartArea = void 0, this._active = [], this._lastEvent = void 0, this._listeners = {}, this._responsiveListeners = void 0, this._sortedMetasets = [], this.scales = {}, this._plugins = new Xf(), this.$proxies = {}, this._hiddenIndices = {}, this.attached = !1, this._animationsDisabled = void 0, this.$context = void 0, this._doResize = Cc((e) => this.update(e), a.resizeDelay || 0), this._dataChanges = [], Op[this.id] = this, !o || !s) {
			console.error("Failed to create chart: can't acquire context from the given item");
			return;
		}
		Lu.listen(this, "complete", Tp), Lu.listen(this, "progress", Ep), this._initialize(), this.attached && this.update();
	}
	get aspectRatio() {
		let { options: { aspectRatio: e, maintainAspectRatio: t }, width: n, height: r, _aspectRatio: i } = this;
		return L(e) ? t && i ? i : r ? n / r : null : e;
	}
	get data() {
		return this.config.data;
	}
	set data(e) {
		this.config.data = e;
	}
	get options() {
		return this._options;
	}
	set options(e) {
		this.config.options = e;
	}
	get registry() {
		return Yf;
	}
	_initialize() {
		return this.notifyPlugins("beforeInit"), this.options.responsive ? this.resize() : du(this, this.options.devicePixelRatio), this.bindEvents(), this.notifyPlugins("afterInit"), this;
	}
	clear() {
		return Qc(this.canvas, this.ctx), this;
	}
	stop() {
		return Lu.stop(this), this;
	}
	resize(e, t) {
		Lu.running(this) ? this._resizeBeforeDraw = {
			width: e,
			height: t
		} : this._resize(e, t);
	}
	_resize(e, t) {
		let n = this.options, r = this.canvas, i = n.maintainAspectRatio && this.aspectRatio, a = this.platform.getMaximumSize(r, e, t, i), o = n.devicePixelRatio || this.platform.getDevicePixelRatio(), s = this.width ? "resize" : "attach";
		this.width = a.width, this.height = a.height, this._aspectRatio = this.aspectRatio, du(this, o, !0) && (this.notifyPlugins("resize", { size: a }), H(n.onResize, [this, a], this), this.attached && this._doResize(s) && this.render());
	}
	ensureScalesHaveIDs() {
		U(this.options.scales || {}, (e, t) => {
			e.id = t;
		});
	}
	buildOrUpdateScales() {
		let e = this.options, t = e.scales, n = this.scales, r = Object.keys(n).reduce((e, t) => (e[t] = !1, e), {}), i = [];
		t && (i = i.concat(Object.keys(t).map((e) => {
			let n = t[e], r = op(e, n), i = r === "r", a = r === "x";
			return {
				options: n,
				dposition: i ? "chartArea" : a ? "bottom" : "left",
				dtype: i ? "radialLinear" : a ? "category" : "linear"
			};
		}))), U(i, (t) => {
			let i = t.options, a = i.id, o = op(a, i), s = V(i.type, t.dtype);
			(i.position === void 0 || Cp(i.position, o) !== Cp(t.dposition)) && (i.position = t.dposition), r[a] = !0;
			let c = null;
			a in n && n[a].type === s ? c = n[a] : (c = new (Yf.getScale(s))({
				id: a,
				type: s,
				ctx: this.ctx,
				chart: this
			}), n[c.id] = c), c.init(i, e);
		}), U(r, (e, t) => {
			e || delete n[t];
		}), U(n, (e) => {
			$d.configure(this, e, e.options), $d.addBox(this, e);
		});
	}
	_updateMetasets() {
		let e = this._metasets, t = this.data.datasets.length, n = e.length;
		if (e.sort((e, t) => e.index - t.index), n > t) {
			for (let e = t; e < n; ++e) this._destroyDatasetMeta(e);
			e.splice(t, n - t);
		}
		this._sortedMetasets = e.slice(0).sort(wp("order", "index"));
	}
	_removeUnreferencedMetasets() {
		let { _metasets: e, data: { datasets: t } } = this;
		e.length > t.length && delete this._stacks, e.forEach((e, n) => {
			t.filter((t) => t === e._dataset).length === 0 && this._destroyDatasetMeta(n);
		});
	}
	buildOrUpdateControllers() {
		let e = [], t = this.data.datasets, n, r;
		for (this._removeUnreferencedMetasets(), n = 0, r = t.length; n < r; n++) {
			let r = t[n], i = this.getDatasetMeta(n), a = r.type || this.config.type;
			if (i.type && i.type !== a && (this._destroyDatasetMeta(n), i = this.getDatasetMeta(n)), i.type = a, i.indexAxis = r.indexAxis || tp(a, this.options), i.order = r.order || 0, i.index = n, i.label = "" + r.label, i.visible = this.isDatasetVisible(n), i.controller) i.controller.updateIndex(n), i.controller.linkScales();
			else {
				let t = Yf.getController(a), { datasetElementType: r, dataElementType: o } = G.datasets[a];
				Object.assign(t, {
					dataElementType: Yf.getElement(o),
					datasetElementType: r && Yf.getElement(r)
				}), i.controller = new t(this, n), e.push(i.controller);
			}
		}
		return this._updateMetasets(), e;
	}
	_resetElements() {
		U(this.data.datasets, (e, t) => {
			this.getDatasetMeta(t).controller.reset();
		}, this);
	}
	reset() {
		this._resetElements(), this.notifyPlugins("reset");
	}
	update(e) {
		let t = this.config;
		t.update();
		let n = this._options = t.createResolver(t.chartOptionScopes(), this.getContext()), r = this._animationsDisabled = !n.animation;
		if (this._updateScales(), this._checkEventBindings(), this._updateHiddenIndices(), this._plugins.invalidate(), this.notifyPlugins("beforeUpdate", {
			mode: e,
			cancelable: !0
		}) === !1) return;
		let i = this.buildOrUpdateControllers();
		this.notifyPlugins("beforeElementsUpdate");
		let a = 0;
		for (let e = 0, t = this.data.datasets.length; e < t; e++) {
			let { controller: t } = this.getDatasetMeta(e), n = !r && i.indexOf(t) === -1;
			t.buildOrUpdateElements(n), a = Math.max(+t.getMaxOverflow(), a);
		}
		a = this._minPadding = n.layout.autoPadding ? a : 0, this._updateLayout(a), r || U(i, (e) => {
			e.reset();
		}), this._updateDatasets(e), this.notifyPlugins("afterUpdate", { mode: e }), this._layers.sort(wp("z", "_idx"));
		let { _active: o, _lastEvent: s } = this;
		s ? this._eventHandler(s, !0) : o.length && this._updateHoverStyles(o, o, !0), this.render();
	}
	_updateScales() {
		U(this.scales, (e) => {
			$d.removeBox(this, e);
		}), this.ensureScalesHaveIDs(), this.buildOrUpdateScales();
	}
	_checkEventBindings() {
		let e = this.options;
		(!Rs(new Set(Object.keys(this._listeners)), new Set(e.events)) || !!this._responsiveListeners !== e.responsive) && (this.unbindEvents(), this.bindEvents());
	}
	_updateHiddenIndices() {
		let { _hiddenIndices: e } = this, t = this._getUniformDataChanges() || [];
		for (let { method: n, start: r, count: i } of t) Ap(e, r, n === "_removeElements" ? -i : i);
	}
	_getUniformDataChanges() {
		let e = this._dataChanges;
		if (!e || !e.length) return;
		this._dataChanges = [];
		let t = this.data.datasets.length, n = (t) => new Set(e.filter((e) => e[0] === t).map((e, t) => t + "," + e.splice(1).join(","))), r = n(0);
		for (let e = 1; e < t; e++) if (!Rs(r, n(e))) return;
		return Array.from(r).map((e) => e.split(",")).map((e) => ({
			method: e[1],
			start: +e[2],
			count: +e[3]
		}));
	}
	_updateLayout(e) {
		if (this.notifyPlugins("beforeLayout", { cancelable: !0 }) === !1) return;
		$d.update(this, this.width, this.height, e);
		let t = this.chartArea, n = t.width <= 0 || t.height <= 0;
		this._layers = [], U(this.boxes, (e) => {
			n && e.position === "chartArea" || (e.configure && e.configure(), this._layers.push(...e._layers()));
		}, this), this._layers.forEach((e, t) => {
			e._idx = t;
		}), this.notifyPlugins("afterLayout");
	}
	_updateDatasets(e) {
		if (this.notifyPlugins("beforeDatasetsUpdate", {
			mode: e,
			cancelable: !0
		}) !== !1) {
			for (let e = 0, t = this.data.datasets.length; e < t; ++e) this.getDatasetMeta(e).controller.configure();
			for (let t = 0, n = this.data.datasets.length; t < n; ++t) this._updateDataset(t, Ls(e) ? e({ datasetIndex: t }) : e);
			this.notifyPlugins("afterDatasetsUpdate", { mode: e });
		}
	}
	_updateDataset(e, t) {
		let n = this.getDatasetMeta(e), r = {
			meta: n,
			index: e,
			mode: t,
			cancelable: !0
		};
		this.notifyPlugins("beforeDatasetUpdate", r) !== !1 && (n.controller._update(t), r.cancelable = !1, this.notifyPlugins("afterDatasetUpdate", r));
	}
	render() {
		this.notifyPlugins("beforeRender", { cancelable: !0 }) !== !1 && (Lu.has(this) ? this.attached && !Lu.running(this) && Lu.start(this) : (this.draw(), Tp({ chart: this })));
	}
	draw() {
		let e;
		if (this._resizeBeforeDraw) {
			let { width: e, height: t } = this._resizeBeforeDraw;
			this._resizeBeforeDraw = null, this._resize(e, t);
		}
		if (this.clear(), this.width <= 0 || this.height <= 0 || this.notifyPlugins("beforeDraw", { cancelable: !0 }) === !1) return;
		let t = this._layers;
		for (e = 0; e < t.length && t[e].z <= 0; ++e) t[e].draw(this.chartArea);
		for (this._drawDatasets(); e < t.length; ++e) t[e].draw(this.chartArea);
		this.notifyPlugins("afterDraw");
	}
	_getSortedDatasetMetas(e) {
		let t = this._sortedMetasets, n = [], r, i;
		for (r = 0, i = t.length; r < i; ++r) {
			let i = t[r];
			(!e || i.visible) && n.push(i);
		}
		return n;
	}
	getSortedVisibleDatasetMetas() {
		return this._getSortedDatasetMetas(!0);
	}
	_drawDatasets() {
		if (this.notifyPlugins("beforeDatasetsDraw", { cancelable: !0 }) === !1) return;
		let e = this.getSortedVisibleDatasetMetas();
		for (let t = e.length - 1; t >= 0; --t) this._drawDataset(e[t]);
		this.notifyPlugins("afterDatasetsDraw");
	}
	_drawDataset(e) {
		let t = this.ctx, n = {
			meta: e,
			index: e.index,
			cancelable: !0
		}, r = Iu(this, e);
		this.notifyPlugins("beforeDatasetDraw", n) !== !1 && (r && nl(t, r), e.controller.draw(), r && rl(t), n.cancelable = !1, this.notifyPlugins("afterDatasetDraw", n));
	}
	isPointInArea(e) {
		return tl(e, this.chartArea, this._minPadding);
	}
	getElementsAtEventForMode(e, t, n, r) {
		let i = Id.modes[t];
		return typeof i == "function" ? i(this, e, n, r) : [];
	}
	getDatasetMeta(e) {
		let t = this.data.datasets[e], n = this._metasets, r = n.filter((e) => e && e._dataset === t).pop();
		return r || (r = {
			type: null,
			data: [],
			dataset: null,
			controller: null,
			hidden: null,
			xAxisID: null,
			yAxisID: null,
			order: t && t.order || 0,
			index: e,
			_dataset: t,
			_parsed: [],
			_sorted: !1
		}, n.push(r)), r;
	}
	getContext() {
		return this.$context ||= Sl(null, {
			chart: this,
			type: "chart"
		});
	}
	getVisibleDatasetCount() {
		return this.getSortedVisibleDatasetMetas().length;
	}
	isDatasetVisible(e) {
		let t = this.data.datasets[e];
		if (!t) return !1;
		let n = this.getDatasetMeta(e);
		return typeof n.hidden == "boolean" ? !n.hidden : !t.hidden;
	}
	setDatasetVisibility(e, t) {
		let n = this.getDatasetMeta(e);
		n.hidden = !t;
	}
	toggleDataVisibility(e) {
		this._hiddenIndices[e] = !this._hiddenIndices[e];
	}
	getDataVisibility(e) {
		return !this._hiddenIndices[e];
	}
	_updateVisibility(e, t, n) {
		let r = n ? "show" : "hide", i = this.getDatasetMeta(e), a = i.controller._resolveAnimations(void 0, r);
		Is(t) ? (i.data[t].hidden = !n, this.update()) : (this.setDatasetVisibility(e, n), a.update(i, { visible: n }), this.update((t) => t.datasetIndex === e ? r : void 0));
	}
	hide(e, t) {
		this._updateVisibility(e, t, !1);
	}
	show(e, t) {
		this._updateVisibility(e, t, !0);
	}
	_destroyDatasetMeta(e) {
		let t = this._metasets[e];
		t && t.controller && t.controller._destroy(), delete this._metasets[e];
	}
	_stop() {
		let e, t;
		for (this.stop(), Lu.remove(this), e = 0, t = this.data.datasets.length; e < t; ++e) this._destroyDatasetMeta(e);
	}
	destroy() {
		this.notifyPlugins("beforeDestroy");
		let { canvas: e, ctx: t } = this;
		this._stop(), this.config.clearCache(), e && (this.unbindEvents(), Qc(e, t), this.platform.releaseContext(t), this.canvas = null, this.ctx = null), delete Op[this.id], this.notifyPlugins("afterDestroy");
	}
	toBase64Image(...e) {
		return this.canvas.toDataURL(...e);
	}
	bindEvents() {
		this.bindUserEvents(), this.options.responsive ? this.bindResponsiveEvents() : this.attached = !0;
	}
	bindUserEvents() {
		let e = this._listeners, t = this.platform, n = (n, r) => {
			t.addEventListener(this, n, r), e[n] = r;
		}, r = (e, t, n) => {
			e.offsetX = t, e.offsetY = n, this._eventHandler(e);
		};
		U(this.options.events, (e) => n(e, r));
	}
	bindResponsiveEvents() {
		this._responsiveListeners ||= {};
		let e = this._responsiveListeners, t = this.platform, n = (n, r) => {
			t.addEventListener(this, n, r), e[n] = r;
		}, r = (n, r) => {
			e[n] && (t.removeEventListener(this, n, r), delete e[n]);
		}, i = (e, t) => {
			this.canvas && this.resize(e, t);
		}, a, o = () => {
			r("attach", o), this.attached = !0, this.resize(), n("resize", i), n("detach", a);
		};
		a = () => {
			this.attached = !1, r("resize", i), this._stop(), this._resize(0, 0), n("attach", o);
		}, t.isAttached(this.canvas) ? o() : a();
	}
	unbindEvents() {
		U(this._listeners, (e, t) => {
			this.platform.removeEventListener(this, t, e);
		}), this._listeners = {}, U(this._responsiveListeners, (e, t) => {
			this.platform.removeEventListener(this, t, e);
		}), this._responsiveListeners = void 0;
	}
	updateHoverStyle(e, t, n) {
		let r = n ? "set" : "remove", i, a, o, s;
		for (t === "dataset" && (i = this.getDatasetMeta(e[0].datasetIndex), i.controller["_" + r + "DatasetHoverStyle"]()), o = 0, s = e.length; o < s; ++o) {
			a = e[o];
			let t = a && this.getDatasetMeta(a.datasetIndex).controller;
			t && t[r + "HoverStyle"](a.element, a.datasetIndex, a.index);
		}
	}
	getActiveElements() {
		return this._active || [];
	}
	setActiveElements(e) {
		let t = this._active || [], n = e.map(({ datasetIndex: e, index: t }) => {
			let n = this.getDatasetMeta(e);
			if (!n) throw Error("No dataset found at index " + e);
			return {
				datasetIndex: e,
				element: n.data[t],
				index: t
			};
		});
		ws(n, t) || (this._active = n, this._lastEvent = null, this._updateHoverStyles(n, t));
	}
	notifyPlugins(e, t, n) {
		return this._plugins.notify(this, e, t, n);
	}
	isPluginEnabled(e) {
		return this._plugins._cache.filter((t) => t.plugin.id === e).length === 1;
	}
	_updateHoverStyles(e, t, n) {
		let r = this.options.hover, i = (e, t) => e.filter((e) => !t.some((t) => e.datasetIndex === t.datasetIndex && e.index === t.index)), a = i(t, e), o = n ? e : i(e, t);
		a.length && this.updateHoverStyle(a, r.mode, !1), o.length && r.mode && this.updateHoverStyle(o, r.mode, !0);
	}
	_eventHandler(e, t) {
		let n = {
			event: e,
			replay: t,
			cancelable: !0,
			inChartArea: this.isPointInArea(e)
		}, r = (t) => (t.options.events || this.options.events).includes(e.native.type);
		if (this.notifyPlugins("beforeEvent", n, r) === !1) return;
		let i = this._handleEvent(e, t, n.inChartArea);
		return n.cancelable = !1, this.notifyPlugins("afterEvent", n, r), (i || n.changed) && this.render(), this;
	}
	_handleEvent(e, t, n) {
		let { _active: r = [], options: i } = this, a = t, o = this._getActiveElements(e, r, n, a), s = zs(e), c = jp(e, this._lastEvent, n, s);
		n && (this._lastEvent = null, H(i.onHover, [
			e,
			o,
			this
		], this), s && H(i.onClick, [
			e,
			o,
			this
		], this));
		let l = !ws(o, r);
		return (l || t) && (this._active = o, this._updateHoverStyles(o, r, t)), this._lastEvent = c, l;
	}
	_getActiveElements(e, t, n, r) {
		if (e.type === "mouseout") return [];
		if (!n) return t;
		let i = this.options.hover;
		return this.getElementsAtEventForMode(e, i.mode, i, r);
	}
};
function Np() {
	return U(Mp.instances, (e) => e._plugins.invalidate());
}
function Pp(e, t, n = t) {
	e.lineCap = V(n.borderCapStyle, t.borderCapStyle), e.setLineDash(V(n.borderDash, t.borderDash)), e.lineDashOffset = V(n.borderDashOffset, t.borderDashOffset), e.lineJoin = V(n.borderJoinStyle, t.borderJoinStyle), e.lineWidth = V(n.borderWidth, t.borderWidth), e.strokeStyle = V(n.borderColor, t.borderColor);
}
function Fp(e, t, n) {
	e.lineTo(n.x, n.y);
}
function Ip(e) {
	return e.stepped ? il : e.tension || e.cubicInterpolationMode === "monotone" ? al : Fp;
}
function Lp(e, t, n = {}) {
	let r = e.length, { start: i = 0, end: a = r - 1 } = n, { start: o, end: s } = t, c = Math.max(i, o), l = Math.min(a, s), u = i < o && a < o || i > s && a > s;
	return {
		count: r,
		start: c,
		loop: t.loop,
		ilen: l < c && !u ? r + l - c : l - c
	};
}
function Rp(e, t, n, r) {
	let { points: i, options: a } = t, { count: o, start: s, loop: c, ilen: l } = Lp(i, n, r), u = Ip(a), { move: d = !0, reverse: f } = r || {}, p, m, h;
	for (p = 0; p <= l; ++p) m = i[(s + (f ? l - p : p)) % o], !m.skip && (d ? (e.moveTo(m.x, m.y), d = !1) : u(e, h, m, f, a.stepped), h = m);
	return c && (m = i[(s + (f ? l : 0)) % o], u(e, h, m, f, a.stepped)), !!c;
}
function zp(e, t, n, r) {
	let i = t.points, { count: a, start: o, ilen: s } = Lp(i, n, r), { move: c = !0, reverse: l } = r || {}, u = 0, d = 0, f, p, m, h, g, _, v = (e) => (o + (l ? s - e : e)) % a, y = () => {
		h !== g && (e.lineTo(u, g), e.lineTo(u, h), e.lineTo(u, _));
	};
	for (c && (p = i[v(0)], e.moveTo(p.x, p.y)), f = 0; f <= s; ++f) {
		if (p = i[v(f)], p.skip) continue;
		let t = p.x, n = p.y, r = t | 0;
		r === m ? (n < h ? h = n : n > g && (g = n), u = (d * u + t) / ++d) : (y(), e.lineTo(t, n), m = r, d = 0, h = g = n), _ = n;
	}
	y();
}
function Bp(e) {
	let t = e.options, n = t.borderDash && t.borderDash.length;
	return !e._decimated && !e._loop && !t.tension && t.cubicInterpolationMode !== "monotone" && !t.stepped && !n ? zp : Rp;
}
function Vp(e) {
	return e.stepped ? hu : e.tension || e.cubicInterpolationMode === "monotone" ? gu : mu;
}
function Hp(e, t, n, r) {
	let i = t._path;
	i || (i = t._path = new Path2D(), t.path(i, n, r) && i.closePath()), Pp(e, t.options), e.stroke(i);
}
function Up(e, t, n, r) {
	let { segments: i, options: a } = t, o = Bp(t);
	for (let s of i) Pp(e, a, s.style), e.beginPath(), o(e, t, s, {
		start: n,
		end: n + r - 1
	}) && e.closePath(), e.stroke();
}
var Wp = typeof Path2D == "function";
function Gp(e, t, n, r) {
	Wp && !t.options.segment ? Hp(e, t, n, r) : Up(e, t, n, r);
}
var Kp = class extends wf {
	static id = "line";
	static defaults = {
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
	};
	static defaultRoutes = {
		backgroundColor: "backgroundColor",
		borderColor: "borderColor"
	};
	static descriptors = {
		_scriptable: !0,
		_indexable: (e) => e !== "borderDash" && e !== "fill"
	};
	constructor(e) {
		super(), this.animated = !0, this.options = void 0, this._chart = void 0, this._loop = void 0, this._fullLoop = void 0, this._path = void 0, this._points = void 0, this._segments = void 0, this._decimated = !1, this._pointsUpdated = !1, this._datasetIndex = void 0, e && Object.assign(this, e);
	}
	updateControlPoints(e, t) {
		let n = this.options;
		if ((n.tension || n.cubicInterpolationMode === "monotone") && !n.stepped && !this._pointsUpdated) {
			let r = n.spanGaps ? this._loop : this._fullLoop;
			Zl(this._points, n, e, r, t), this._pointsUpdated = !0;
		}
	}
	set points(e) {
		this._points = e, delete this._segments, delete this._path, this._pointsUpdated = !1;
	}
	get points() {
		return this._points;
	}
	get segments() {
		return this._segments ||= ku(this, this.options.segment);
	}
	first() {
		let e = this.segments, t = this.points;
		return e.length && t[e[0].start];
	}
	last() {
		let e = this.segments, t = this.points, n = e.length;
		return n && t[e[n - 1].end];
	}
	interpolate(e, t) {
		let n = this.options, r = e[t], i = this.points, a = Eu(this, {
			property: t,
			start: r,
			end: r
		});
		if (!a.length) return;
		let o = [], s = Vp(n), c, l;
		for (c = 0, l = a.length; c < l; ++c) {
			let { start: l, end: u } = a[c], d = i[l], f = i[u];
			if (d === f) {
				o.push(d);
				continue;
			}
			let p = s(d, f, Math.abs((r - d[t]) / (f[t] - d[t])), n.stepped);
			p[t] = e[t], o.push(p);
		}
		return o.length === 1 ? o[0] : o;
	}
	pathSegment(e, t, n) {
		return Bp(this)(e, this, t, n);
	}
	path(e, t, n) {
		let r = this.segments, i = Bp(this), a = this._loop;
		t ||= 0, n ||= this.points.length - t;
		for (let o of r) a &= i(e, this, o, {
			start: t,
			end: t + n - 1
		});
		return !!a;
	}
	draw(e, t, n, r) {
		let i = this.options || {};
		(this.points || []).length && i.borderWidth && (e.save(), Gp(e, this, n, r), e.restore()), this.animated && (this._pointsUpdated = !1, this._path = void 0);
	}
};
function qp(e, t, n, r) {
	let i = e.options, { [n]: a } = e.getProps([n], r);
	return Math.abs(t - a) < i.radius + i.hitRadius;
}
var Jp = class extends wf {
	static id = "point";
	parsed;
	skip;
	stop;
	static defaults = {
		borderWidth: 1,
		hitRadius: 1,
		hoverBorderWidth: 1,
		hoverRadius: 4,
		pointStyle: "circle",
		radius: 3,
		rotation: 0
	};
	static defaultRoutes = {
		backgroundColor: "backgroundColor",
		borderColor: "borderColor"
	};
	constructor(e) {
		super(), this.options = void 0, this.parsed = void 0, this.skip = void 0, this.stop = void 0, e && Object.assign(this, e);
	}
	inRange(e, t, n) {
		let r = this.options, { x: i, y: a } = this.getProps(["x", "y"], n);
		return (e - i) ** 2 + (t - a) ** 2 < (r.hitRadius + r.radius) ** 2;
	}
	inXRange(e, t) {
		return qp(this, e, "x", t);
	}
	inYRange(e, t) {
		return qp(this, e, "y", t);
	}
	getCenterPoint(e) {
		let { x: t, y: n } = this.getProps(["x", "y"], e);
		return {
			x: t,
			y: n
		};
	}
	size(e) {
		e = e || this.options || {};
		let t = e.radius || 0;
		t = Math.max(t, t && e.hoverRadius || 0);
		let n = t && e.borderWidth || 0;
		return (t + n) * 2;
	}
	draw(e, t) {
		let n = this.options;
		this.skip || n.radius < .1 || !tl(this, t, this.size(n) / 2) || (e.strokeStyle = n.borderColor, e.lineWidth = n.borderWidth, e.fillStyle = n.backgroundColor, $c(e, n, this.x, this.y));
	}
	getRange() {
		let e = this.options || {};
		return e.radius + e.hitRadius;
	}
};
function Yp(e, t) {
	let { x: n, y: r, base: i, width: a, height: o } = e.getProps([
		"x",
		"y",
		"base",
		"width",
		"height"
	], t), s, c, l, u, d;
	return e.horizontal ? (d = o / 2, s = Math.min(n, i), c = Math.max(n, i), l = r - d, u = r + d) : (d = a / 2, s = n - d, c = n + d, l = Math.min(r, i), u = Math.max(r, i)), {
		left: s,
		top: l,
		right: c,
		bottom: u
	};
}
function Xp(e, t, n, r) {
	return e ? 0 : uc(t, n, r);
}
function Zp(e, t, n) {
	let r = e.options.borderWidth, i = e.borderSkipped, a = gl(r);
	return {
		t: Xp(i.top, a.top, 0, n),
		r: Xp(i.right, a.right, 0, t),
		b: Xp(i.bottom, a.bottom, 0, n),
		l: Xp(i.left, a.left, 0, t)
	};
}
function Qp(e, t, n) {
	let { enableBorderRadius: r } = e.getProps(["enableBorderRadius"]), i = e.options.borderRadius, a = _l(i), o = Math.min(t, n), s = e.borderSkipped, c = r || z(i);
	return {
		topLeft: Xp(!c || s.top || s.left, a.topLeft, 0, o),
		topRight: Xp(!c || s.top || s.right, a.topRight, 0, o),
		bottomLeft: Xp(!c || s.bottom || s.left, a.bottomLeft, 0, o),
		bottomRight: Xp(!c || s.bottom || s.right, a.bottomRight, 0, o)
	};
}
function $p(e) {
	let t = Yp(e), n = t.right - t.left, r = t.bottom - t.top, i = Zp(e, n / 2, r / 2), a = Qp(e, n / 2, r / 2);
	return {
		outer: {
			x: t.left,
			y: t.top,
			w: n,
			h: r,
			radius: a
		},
		inner: {
			x: t.left + i.l,
			y: t.top + i.t,
			w: n - i.l - i.r,
			h: r - i.t - i.b,
			radius: {
				topLeft: Math.max(0, a.topLeft - Math.max(i.t, i.l)),
				topRight: Math.max(0, a.topRight - Math.max(i.t, i.r)),
				bottomLeft: Math.max(0, a.bottomLeft - Math.max(i.b, i.l)),
				bottomRight: Math.max(0, a.bottomRight - Math.max(i.b, i.r))
			}
		}
	};
}
function em(e, t, n, r) {
	let i = t === null, a = n === null, o = e && !(i && a) && Yp(e, r);
	return o && (i || fc(t, o.left, o.right)) && (a || fc(n, o.top, o.bottom));
}
function tm(e) {
	return e.topLeft || e.topRight || e.bottomLeft || e.bottomRight;
}
function nm(e, t) {
	e.rect(t.x, t.y, t.w, t.h);
}
function rm(e, t, n = {}) {
	let r = e.x === n.x ? 0 : -t, i = e.y === n.y ? 0 : -t, a = (e.x + e.w === n.x + n.w ? 0 : t) - r, o = (e.y + e.h === n.y + n.h ? 0 : t) - i;
	return {
		x: e.x + r,
		y: e.y + i,
		w: e.w + a,
		h: e.h + o,
		radius: e.radius
	};
}
var im = class extends wf {
	static id = "bar";
	static defaults = {
		borderSkipped: "start",
		borderWidth: 0,
		borderRadius: 0,
		inflateAmount: "auto",
		pointStyle: void 0
	};
	static defaultRoutes = {
		backgroundColor: "backgroundColor",
		borderColor: "borderColor"
	};
	constructor(e) {
		super(), this.options = void 0, this.horizontal = void 0, this.base = void 0, this.width = void 0, this.height = void 0, this.inflateAmount = void 0, e && Object.assign(this, e);
	}
	draw(e) {
		let { inflateAmount: t, options: { borderColor: n, backgroundColor: r } } = this, { inner: i, outer: a } = $p(this), o = tm(a.radius) ? ul : nm;
		e.save(), (a.w !== i.w || a.h !== i.h) && (e.beginPath(), o(e, rm(a, t, i)), e.clip(), o(e, rm(i, -t, a)), e.fillStyle = n, e.fill("evenodd")), e.beginPath(), o(e, rm(i, t)), e.fillStyle = r, e.fill(), e.restore();
	}
	inRange(e, t, n) {
		return em(this, e, t, n);
	}
	inXRange(e, t) {
		return em(this, e, null, t);
	}
	inYRange(e, t) {
		return em(this, null, e, t);
	}
	getCenterPoint(e) {
		let { x: t, y: n, base: r, horizontal: i } = this.getProps([
			"x",
			"y",
			"base",
			"horizontal"
		], e);
		return {
			x: i ? (t + r) / 2 : t,
			y: i ? n : (n + r) / 2
		};
	}
	getRange(e) {
		return e === "x" ? this.width / 2 : this.height / 2;
	}
};
function am(e, t, n) {
	let r = e.segments, i = e.points, a = t.points, o = [];
	for (let e of r) {
		let { start: r, end: s } = e;
		s = cm(r, s, i);
		let c = om(n, i[r], i[s], e.loop);
		if (!t.segments) {
			o.push({
				source: e,
				target: c,
				start: i[r],
				end: i[s]
			});
			continue;
		}
		let l = Eu(t, c);
		for (let t of l) {
			let r = om(n, a[t.start], a[t.end], t.loop), s = Tu(e, i, r);
			for (let e of s) o.push({
				source: e,
				target: t,
				start: { [n]: lm(c, r, "start", Math.max) },
				end: { [n]: lm(c, r, "end", Math.min) }
			});
		}
	}
	return o;
}
function om(e, t, n, r) {
	if (r) return;
	let i = t[e], a = n[e];
	return e === "angle" && (i = cc(i), a = cc(a)), {
		property: e,
		start: i,
		end: a
	};
}
function sm(e, t) {
	let { x: n = null, y: r = null } = e || {}, i = t.points, a = [];
	return t.segments.forEach(({ start: e, end: t }) => {
		t = cm(e, t, i);
		let o = i[e], s = i[t];
		r === null ? n !== null && (a.push({
			x: n,
			y: o.y
		}), a.push({
			x: n,
			y: s.y
		})) : (a.push({
			x: o.x,
			y: r
		}), a.push({
			x: s.x,
			y: r
		}));
	}), a;
}
function cm(e, t, n) {
	for (; t > e; t--) {
		let e = n[t];
		if (!isNaN(e.x) && !isNaN(e.y)) break;
	}
	return t;
}
function lm(e, t, n, r) {
	return e && t ? r(e[n], t[n]) : e ? e[n] : t ? t[n] : 0;
}
function um(e, t) {
	let n = [], r = !1;
	return R(e) ? (r = !0, n = e) : n = sm(e, t), n.length ? new Kp({
		points: n,
		options: { tension: 0 },
		_loop: r,
		_fullLoop: r
	}) : null;
}
function dm(e) {
	return e && e.fill !== !1;
}
function fm(e, t, n) {
	let r = e[t].fill, i = [t], a;
	if (!n) return r;
	for (; r !== !1 && i.indexOf(r) === -1;) {
		if (!B(r)) return r;
		if (a = e[r], !a) return !1;
		if (a.visible) return r;
		i.push(r), r = a.fill;
	}
	return !1;
}
function pm(e, t, n) {
	let r = _m(e);
	if (z(r)) return isNaN(r.value) ? !1 : r;
	let i = parseFloat(r);
	return B(i) && Math.floor(i) === i ? mm(r[0], t, i, n) : [
		"origin",
		"start",
		"end",
		"stack",
		"shape"
	].indexOf(r) >= 0 && r;
}
function mm(e, t, n, r) {
	return (e === "-" || e === "+") && (n = t + n), n === t || n < 0 || n >= r ? !1 : n;
}
function hm(e, t) {
	let n = null;
	return e === "start" ? n = t.bottom : e === "end" ? n = t.top : z(e) ? n = t.getPixelForValue(e.value) : t.getBasePixel && (n = t.getBasePixel()), n;
}
function gm(e, t, n) {
	let r;
	return r = e === "start" ? n : e === "end" ? t.options.reverse ? t.min : t.max : z(e) ? e.value : t.getBaseValue(), r;
}
function _m(e) {
	let t = e.options, n = t.fill, r = V(n && n.target, n);
	return r === void 0 && (r = !!t.backgroundColor), r === !1 || r === null ? !1 : r === !0 ? "origin" : r;
}
function vm(e) {
	let { scale: t, index: n, line: r } = e, i = [], a = r.segments, o = r.points, s = ym(t, n);
	s.push(um({
		x: null,
		y: t.bottom
	}, r));
	for (let e = 0; e < a.length; e++) {
		let t = a[e];
		for (let e = t.start; e <= t.end; e++) bm(i, o[e], s);
	}
	return new Kp({
		points: i,
		options: {}
	});
}
function ym(e, t) {
	let n = [], r = e.getMatchingVisibleMetas("line");
	for (let e = 0; e < r.length; e++) {
		let i = r[e];
		if (i.index === t) break;
		i.hidden || n.unshift(i.dataset);
	}
	return n;
}
function bm(e, t, n) {
	let r = [];
	for (let i = 0; i < n.length; i++) {
		let a = n[i], { first: o, last: s, point: c } = xm(a, t, "x");
		if (!(!c || o && s)) {
			if (o) r.unshift(c);
			else if (e.push(c), !s) break;
		}
	}
	e.push(...r);
}
function xm(e, t, n) {
	let r = e.interpolate(t, n);
	if (!r) return {};
	let i = r[n], a = e.segments, o = e.points, s = !1, c = !1;
	for (let e = 0; e < a.length; e++) {
		let t = a[e], r = o[t.start][n], l = o[t.end][n];
		if (fc(i, r, l)) {
			s = i === r, c = i === l;
			break;
		}
	}
	return {
		first: s,
		last: c,
		point: r
	};
}
var Sm = class {
	constructor(e) {
		this.x = e.x, this.y = e.y, this.radius = e.radius;
	}
	pathSegment(e, t, n) {
		let { x: r, y: i, radius: a } = this;
		return t ||= {
			start: 0,
			end: Bs
		}, e.arc(r, i, a, t.end, t.start, !0), !n.bounds;
	}
	interpolate(e) {
		let { x: t, y: n, radius: r } = this, i = e.angle;
		return {
			x: t + Math.cos(i) * r,
			y: n + Math.sin(i) * r,
			angle: i
		};
	}
};
function Cm(e) {
	let { chart: t, fill: n, line: r } = e;
	if (B(n)) return wm(t, n);
	if (n === "stack") return vm(e);
	if (n === "shape") return !0;
	let i = Tm(e);
	return i instanceof Sm ? i : um(i, r);
}
function wm(e, t) {
	let n = e.getDatasetMeta(t);
	return n && e.isDatasetVisible(t) ? n.dataset : null;
}
function Tm(e) {
	return (e.scale || {}).getPointPositionForValue ? Dm(e) : Em(e);
}
function Em(e) {
	let { scale: t = {}, fill: n } = e, r = hm(n, t);
	if (B(r)) {
		let e = t.isHorizontal();
		return {
			x: e ? r : null,
			y: e ? null : r
		};
	}
	return null;
}
function Dm(e) {
	let { scale: t, fill: n } = e, r = t.options, i = t.getLabels().length, a = r.reverse ? t.max : t.min, o = gm(n, t, a), s = [];
	if (r.grid.circular) {
		let e = t.getPointPositionForValue(0, a);
		return new Sm({
			x: e.x,
			y: e.y,
			radius: t.getDistanceFromCenterForValue(o)
		});
	}
	for (let e = 0; e < i; ++e) s.push(t.getPointPositionForValue(e, o));
	return s;
}
function Om(e, t, n) {
	let r = Cm(t), { chart: i, index: a, line: o, scale: s, axis: c } = t, l = o.options, u = l.fill, d = l.backgroundColor, { above: f = d, below: p = d } = u || {}, m = Iu(i, i.getDatasetMeta(a));
	r && o.points.length && (nl(e, n), km(e, {
		line: o,
		target: r,
		above: f,
		below: p,
		area: n,
		scale: s,
		axis: c,
		clip: m
	}), rl(e));
}
function km(e, t) {
	let { line: n, target: r, above: i, below: a, area: o, scale: s, clip: c } = t, l = n._loop ? "angle" : t.axis;
	e.save();
	let u = a;
	a !== i && (l === "x" ? (Am(e, r, o.top), Mm(e, {
		line: n,
		target: r,
		color: i,
		scale: s,
		property: l,
		clip: c
	}), e.restore(), e.save(), Am(e, r, o.bottom)) : l === "y" && (jm(e, r, o.left), Mm(e, {
		line: n,
		target: r,
		color: a,
		scale: s,
		property: l,
		clip: c
	}), e.restore(), e.save(), jm(e, r, o.right), u = i)), Mm(e, {
		line: n,
		target: r,
		color: u,
		scale: s,
		property: l,
		clip: c
	}), e.restore();
}
function Am(e, t, n) {
	let { segments: r, points: i } = t, a = !0, o = !1;
	e.beginPath();
	for (let s of r) {
		let { start: r, end: c } = s, l = i[r], u = i[cm(r, c, i)];
		a ? (e.moveTo(l.x, l.y), a = !1) : (e.lineTo(l.x, n), e.lineTo(l.x, l.y)), o = !!t.pathSegment(e, s, { move: o }), o ? e.closePath() : e.lineTo(u.x, n);
	}
	e.lineTo(t.first().x, n), e.closePath(), e.clip();
}
function jm(e, t, n) {
	let { segments: r, points: i } = t, a = !0, o = !1;
	e.beginPath();
	for (let s of r) {
		let { start: r, end: c } = s, l = i[r], u = i[cm(r, c, i)];
		a ? (e.moveTo(l.x, l.y), a = !1) : (e.lineTo(n, l.y), e.lineTo(l.x, l.y)), o = !!t.pathSegment(e, s, { move: o }), o ? e.closePath() : e.lineTo(n, u.y);
	}
	e.lineTo(n, t.first().y), e.closePath(), e.clip();
}
function Mm(e, t) {
	let { line: n, target: r, property: i, color: a, scale: o, clip: s } = t, c = am(n, r, i);
	for (let { source: t, target: l, start: u, end: d } of c) {
		let { style: { backgroundColor: c = a } = {} } = t, f = r !== !0;
		e.save(), e.fillStyle = c, Nm(e, o, s, f && om(i, u, d)), e.beginPath();
		let p = !!n.pathSegment(e, t), m;
		if (f) {
			p ? e.closePath() : Pm(e, r, d, i);
			let t = !!r.pathSegment(e, l, {
				move: p,
				reverse: !0
			});
			m = p && t, m || Pm(e, r, u, i);
		}
		e.closePath(), e.fill(m ? "evenodd" : "nonzero"), e.restore();
	}
}
function Nm(e, t, n, r) {
	let i = t.chart.chartArea, { property: a, start: o, end: s } = r || {};
	if (a === "x" || a === "y") {
		let t, r, c, l;
		a === "x" ? (t = o, r = i.top, c = s, l = i.bottom) : (t = i.left, r = o, c = i.right, l = s), e.beginPath(), n && (t = Math.max(t, n.left), c = Math.min(c, n.right), r = Math.max(r, n.top), l = Math.min(l, n.bottom)), e.rect(t, r, c - t, l - r), e.clip();
	}
}
function Pm(e, t, n, r) {
	let i = t.interpolate(n, r);
	i && e.lineTo(i.x, i.y);
}
var Fm = {
	id: "filler",
	afterDatasetsUpdate(e, t, n) {
		let r = (e.data.datasets || []).length, i = [], a, o, s, c;
		for (o = 0; o < r; ++o) a = e.getDatasetMeta(o), s = a.dataset, c = null, s && s.options && s instanceof Kp && (c = {
			visible: e.isDatasetVisible(o),
			index: o,
			fill: pm(s, o, r),
			chart: e,
			axis: a.controller.options.indexAxis,
			scale: a.vScale,
			line: s
		}), a.$filler = c, i.push(c);
		for (o = 0; o < r; ++o) c = i[o], !(!c || c.fill === !1) && (c.fill = fm(i, o, n.propagate));
	},
	beforeDraw(e, t, n) {
		let r = n.drawTime === "beforeDraw", i = e.getSortedVisibleDatasetMetas(), a = e.chartArea;
		for (let t = i.length - 1; t >= 0; --t) {
			let n = i[t].$filler;
			n && (n.line.updateControlPoints(a, n.axis), r && n.fill && Om(e.ctx, n, a));
		}
	},
	beforeDatasetsDraw(e, t, n) {
		if (n.drawTime !== "beforeDatasetsDraw") return;
		let r = e.getSortedVisibleDatasetMetas();
		for (let t = r.length - 1; t >= 0; --t) {
			let n = r[t].$filler;
			dm(n) && Om(e.ctx, n, e.chartArea);
		}
	},
	beforeDatasetDraw(e, t, n) {
		let r = t.meta.$filler;
		!dm(r) || n.drawTime !== "beforeDatasetDraw" || Om(e.ctx, r, e.chartArea);
	},
	defaults: {
		propagate: !0,
		drawTime: "beforeDatasetDraw"
	}
}, Im = {
	average(e) {
		if (!e.length) return !1;
		let t, n, r = /* @__PURE__ */ new Set(), i = 0, a = 0;
		for (t = 0, n = e.length; t < n; ++t) {
			let n = e[t].element;
			if (n && n.hasValue()) {
				let e = n.tooltipPosition();
				r.add(e.x), i += e.y, ++a;
			}
		}
		return a === 0 || r.size === 0 ? !1 : {
			x: [...r].reduce((e, t) => e + t) / r.size,
			y: i / a
		};
	},
	nearest(e, t) {
		if (!e.length) return !1;
		let n = t.x, r = t.y, i = Infinity, a, o, s;
		for (a = 0, o = e.length; a < o; ++a) {
			let n = e[a].element;
			if (n && n.hasValue()) {
				let e = oc(t, n.getCenterPoint());
				e < i && (i = e, s = n);
			}
		}
		if (s) {
			let e = s.tooltipPosition();
			n = e.x, r = e.y;
		}
		return {
			x: n,
			y: r
		};
	}
};
function Lm(e, t) {
	return t && (R(t) ? Array.prototype.push.apply(e, t) : e.push(t)), e;
}
function Rm(e) {
	return (typeof e == "string" || e instanceof String) && e.indexOf("\n") > -1 ? e.split("\n") : e;
}
function zm(e, t) {
	let { element: n, datasetIndex: r, index: i } = t, a = e.getDatasetMeta(r).controller, { label: o, value: s } = a.getLabelAndValue(i);
	return {
		chart: e,
		label: o,
		parsed: a.getParsed(i),
		raw: e.data.datasets[r].data[i],
		formattedValue: s,
		dataset: a.getDataset(),
		dataIndex: i,
		datasetIndex: r,
		element: n
	};
}
function Bm(e, t) {
	let n = e.chart.ctx, { body: r, footer: i, title: a } = e, { boxWidth: o, boxHeight: s } = t, c = yl(t.bodyFont), l = yl(t.titleFont), u = yl(t.footerFont), d = a.length, f = i.length, p = r.length, m = vl(t.padding), h = m.height, g = 0, _ = r.reduce((e, t) => e + t.before.length + t.lines.length + t.after.length, 0);
	if (_ += e.beforeBody.length + e.afterBody.length, d && (h += d * l.lineHeight + (d - 1) * t.titleSpacing + t.titleMarginBottom), _) {
		let e = t.displayColors ? Math.max(s, c.lineHeight) : c.lineHeight;
		h += p * e + (_ - p) * c.lineHeight + (_ - 1) * t.bodySpacing;
	}
	f && (h += t.footerMarginTop + f * u.lineHeight + (f - 1) * t.footerSpacing);
	let v = 0, y = function(e) {
		g = Math.max(g, n.measureText(e).width + v);
	};
	return n.save(), n.font = l.string, U(e.title, y), n.font = c.string, U(e.beforeBody.concat(e.afterBody), y), v = t.displayColors ? o + 2 + t.boxPadding : 0, U(r, (e) => {
		U(e.before, y), U(e.lines, y), U(e.after, y);
	}), v = 0, n.font = u.string, U(e.footer, y), n.restore(), g += m.width, {
		width: g,
		height: h
	};
}
function Vm(e, t) {
	let { y: n, height: r } = t;
	return n < r / 2 ? "top" : n > e.height - r / 2 ? "bottom" : "center";
}
function Hm(e, t, n, r) {
	let { x: i, width: a } = r, o = n.caretSize + n.caretPadding;
	if (e === "left" && i + a + o > t.width || e === "right" && i - a - o < 0) return !0;
}
function Um(e, t, n, r) {
	let { x: i, width: a } = n, { width: o, chartArea: { left: s, right: c } } = e, l = "center";
	return r === "center" ? l = i <= (s + c) / 2 ? "left" : "right" : i <= a / 2 ? l = "left" : i >= o - a / 2 && (l = "right"), Hm(l, e, t, n) && (l = "center"), l;
}
function Wm(e, t, n) {
	let r = n.yAlign || t.yAlign || Vm(e, n);
	return {
		xAlign: n.xAlign || t.xAlign || Um(e, t, n, r),
		yAlign: r
	};
}
function Gm(e, t) {
	let { x: n, width: r } = e;
	return t === "right" ? n -= r : t === "center" && (n -= r / 2), n;
}
function Km(e, t, n) {
	let { y: r, height: i } = e;
	return t === "top" ? r += n : t === "bottom" ? r -= i + n : r -= i / 2, r;
}
function qm(e, t, n, r) {
	let { caretSize: i, caretPadding: a, cornerRadius: o } = e, { xAlign: s, yAlign: c } = n, l = i + a, { topLeft: u, topRight: d, bottomLeft: f, bottomRight: p } = _l(o), m = Gm(t, s), h = Km(t, c, l);
	return c === "center" ? s === "left" ? m += l : s === "right" && (m -= l) : s === "left" ? m -= Math.max(u, f) + i : s === "right" && (m += Math.max(d, p) + i), {
		x: uc(m, 0, r.width - t.width),
		y: uc(h, 0, r.height - t.height)
	};
}
function Jm(e, t, n) {
	let r = vl(n.padding);
	return t === "center" ? e.x + e.width / 2 : t === "right" ? e.x + e.width - r.right : e.x + r.left;
}
function Ym(e) {
	return Lm([], Rm(e));
}
function Xm(e, t, n) {
	return Sl(e, {
		tooltip: t,
		tooltipItems: n,
		type: "tooltip"
	});
}
function Zm(e, t) {
	let n = t && t.dataset && t.dataset.tooltip && t.dataset.tooltip.callbacks;
	return n ? e.override(n) : e;
}
var Qm = {
	beforeTitle: bs,
	title(e) {
		if (e.length > 0) {
			let t = e[0], n = t.chart.data.labels, r = n ? n.length : 0;
			if (this && this.options && this.options.mode === "dataset") return t.dataset.label || "";
			if (t.label) return t.label;
			if (r > 0 && t.dataIndex < r) return n[t.dataIndex];
		}
		return "";
	},
	afterTitle: bs,
	beforeBody: bs,
	beforeLabel: bs,
	label(e) {
		if (this && this.options && this.options.mode === "dataset") return e.label + ": " + e.formattedValue || e.formattedValue;
		let t = e.dataset.label || "";
		t && (t += ": ");
		let n = e.formattedValue;
		return L(n) || (t += n), t;
	},
	labelColor(e) {
		let t = e.chart.getDatasetMeta(e.datasetIndex).controller.getStyle(e.dataIndex);
		return {
			borderColor: t.borderColor,
			backgroundColor: t.backgroundColor,
			borderWidth: t.borderWidth,
			borderDash: t.borderDash,
			borderDashOffset: t.borderDashOffset,
			borderRadius: 0
		};
	},
	labelTextColor() {
		return this.options.bodyColor;
	},
	labelPointStyle(e) {
		let t = e.chart.getDatasetMeta(e.datasetIndex).controller.getStyle(e.dataIndex);
		return {
			pointStyle: t.pointStyle,
			rotation: t.rotation
		};
	},
	afterLabel: bs,
	afterBody: bs,
	beforeFooter: bs,
	footer: bs,
	afterFooter: bs
};
function $m(e, t, n, r) {
	let i = e[t].call(n, r);
	return i === void 0 ? Qm[t].call(n, r) : i;
}
var eh = class extends wf {
	static positioners = Im;
	constructor(e) {
		super(), this.opacity = 0, this._active = [], this._eventPosition = void 0, this._size = void 0, this._cachedAnimations = void 0, this._tooltipItems = [], this.$animations = void 0, this.$context = void 0, this.chart = e.chart, this.options = e.options, this.dataPoints = void 0, this.title = void 0, this.beforeBody = void 0, this.body = void 0, this.afterBody = void 0, this.footer = void 0, this.xAlign = void 0, this.yAlign = void 0, this.x = void 0, this.y = void 0, this.height = void 0, this.width = void 0, this.caretX = void 0, this.caretY = void 0, this.labelColors = void 0, this.labelPointStyles = void 0, this.labelTextColors = void 0;
	}
	initialize(e) {
		this.options = e, this._cachedAnimations = void 0, this.$context = void 0;
	}
	_resolveAnimations() {
		let e = this._cachedAnimations;
		if (e) return e;
		let t = this.chart, n = this.options.setContext(this.getContext()), r = n.enabled && t.options.animation && n.animations, i = new Vu(this.chart, r);
		return r._cacheable && (this._cachedAnimations = Object.freeze(i)), i;
	}
	getContext() {
		return this.$context ||= Xm(this.chart.getContext(), this, this._tooltipItems);
	}
	getTitle(e, t) {
		let { callbacks: n } = t, r = $m(n, "beforeTitle", this, e), i = $m(n, "title", this, e), a = $m(n, "afterTitle", this, e), o = [];
		return o = Lm(o, Rm(r)), o = Lm(o, Rm(i)), o = Lm(o, Rm(a)), o;
	}
	getBeforeBody(e, t) {
		return Ym($m(t.callbacks, "beforeBody", this, e));
	}
	getBody(e, t) {
		let { callbacks: n } = t, r = [];
		return U(e, (e) => {
			let t = {
				before: [],
				lines: [],
				after: []
			}, i = Zm(n, e);
			Lm(t.before, Rm($m(i, "beforeLabel", this, e))), Lm(t.lines, $m(i, "label", this, e)), Lm(t.after, Rm($m(i, "afterLabel", this, e))), r.push(t);
		}), r;
	}
	getAfterBody(e, t) {
		return Ym($m(t.callbacks, "afterBody", this, e));
	}
	getFooter(e, t) {
		let { callbacks: n } = t, r = $m(n, "beforeFooter", this, e), i = $m(n, "footer", this, e), a = $m(n, "afterFooter", this, e), o = [];
		return o = Lm(o, Rm(r)), o = Lm(o, Rm(i)), o = Lm(o, Rm(a)), o;
	}
	_createItems(e) {
		let t = this._active, n = this.chart.data, r = [], i = [], a = [], o = [], s, c;
		for (s = 0, c = t.length; s < c; ++s) o.push(zm(this.chart, t[s]));
		return e.filter && (o = o.filter((t, r, i) => e.filter(t, r, i, n))), e.itemSort && (o = o.sort((t, r) => e.itemSort(t, r, n))), U(o, (t) => {
			let n = Zm(e.callbacks, t);
			r.push($m(n, "labelColor", this, t)), i.push($m(n, "labelPointStyle", this, t)), a.push($m(n, "labelTextColor", this, t));
		}), this.labelColors = r, this.labelPointStyles = i, this.labelTextColors = a, this.dataPoints = o, o;
	}
	update(e, t) {
		let n = this.options.setContext(this.getContext()), r = this._active, i, a = [];
		if (!r.length) this.opacity !== 0 && (i = { opacity: 0 });
		else {
			let e = Im[n.position].call(this, r, this._eventPosition);
			a = this._createItems(n), this.title = this.getTitle(a, n), this.beforeBody = this.getBeforeBody(a, n), this.body = this.getBody(a, n), this.afterBody = this.getAfterBody(a, n), this.footer = this.getFooter(a, n);
			let t = this._size = Bm(this, n), o = Object.assign({}, e, t), s = Wm(this.chart, n, o), c = qm(n, o, s, this.chart);
			this.xAlign = s.xAlign, this.yAlign = s.yAlign, i = {
				opacity: 1,
				x: c.x,
				y: c.y,
				width: t.width,
				height: t.height,
				caretX: e.x,
				caretY: e.y
			};
		}
		this._tooltipItems = a, this.$context = void 0, i && this._resolveAnimations().update(this, i), e && n.external && n.external.call(this, {
			chart: this.chart,
			tooltip: this,
			replay: t
		});
	}
	drawCaret(e, t, n, r) {
		let i = this.getCaretPosition(e, n, r);
		t.lineTo(i.x1, i.y1), t.lineTo(i.x2, i.y2), t.lineTo(i.x3, i.y3);
	}
	getCaretPosition(e, t, n) {
		let { xAlign: r, yAlign: i } = this, { caretSize: a, cornerRadius: o } = n, { topLeft: s, topRight: c, bottomLeft: l, bottomRight: u } = _l(o), { x: d, y: f } = e, { width: p, height: m } = t, h, g, _, v, y, b;
		return i === "center" ? (y = f + m / 2, r === "left" ? (h = d, g = h - a, v = y + a, b = y - a) : (h = d + p, g = h + a, v = y - a, b = y + a), _ = h) : (g = r === "left" ? d + Math.max(s, l) + a : r === "right" ? d + p - Math.max(c, u) - a : this.caretX, i === "top" ? (v = f, y = v - a, h = g - a, _ = g + a) : (v = f + m, y = v + a, h = g + a, _ = g - a), b = v), {
			x1: h,
			x2: g,
			x3: _,
			y1: v,
			y2: y,
			y3: b
		};
	}
	drawTitle(e, t, n) {
		let r = this.title, i = r.length, a, o, s;
		if (i) {
			let c = yu(n.rtl, this.x, this.width);
			for (e.x = Jm(this, n.titleAlign, n), t.textAlign = c.textAlign(n.titleAlign), t.textBaseline = "middle", a = yl(n.titleFont), o = n.titleSpacing, t.fillStyle = n.titleColor, t.font = a.string, s = 0; s < i; ++s) t.fillText(r[s], c.x(e.x), e.y + a.lineHeight / 2), e.y += a.lineHeight + o, s + 1 === i && (e.y += n.titleMarginBottom - o);
		}
	}
	_drawColorBox(e, t, n, r, i) {
		let a = this.labelColors[n], o = this.labelPointStyles[n], { boxHeight: s, boxWidth: c } = i, l = yl(i.bodyFont), u = Jm(this, "left", i), d = r.x(u), f = s < l.lineHeight ? (l.lineHeight - s) / 2 : 0, p = t.y + f;
		if (i.usePointStyle) {
			let t = {
				radius: Math.min(c, s) / 2,
				pointStyle: o.pointStyle,
				rotation: o.rotation,
				borderWidth: 1
			}, n = r.leftForLtr(d, c) + c / 2, l = p + s / 2;
			e.strokeStyle = i.multiKeyBackground, e.fillStyle = i.multiKeyBackground, $c(e, t, n, l), e.strokeStyle = a.borderColor, e.fillStyle = a.backgroundColor, $c(e, t, n, l);
		} else {
			e.lineWidth = z(a.borderWidth) ? Math.max(...Object.values(a.borderWidth)) : a.borderWidth || 1, e.strokeStyle = a.borderColor, e.setLineDash(a.borderDash || []), e.lineDashOffset = a.borderDashOffset || 0;
			let t = r.leftForLtr(d, c), n = r.leftForLtr(r.xPlus(d, 1), c - 2), o = _l(a.borderRadius);
			Object.values(o).some((e) => e !== 0) ? (e.beginPath(), e.fillStyle = i.multiKeyBackground, ul(e, {
				x: t,
				y: p,
				w: c,
				h: s,
				radius: o
			}), e.fill(), e.stroke(), e.fillStyle = a.backgroundColor, e.beginPath(), ul(e, {
				x: n,
				y: p + 1,
				w: c - 2,
				h: s - 2,
				radius: o
			}), e.fill()) : (e.fillStyle = i.multiKeyBackground, e.fillRect(t, p, c, s), e.strokeRect(t, p, c, s), e.fillStyle = a.backgroundColor, e.fillRect(n, p + 1, c - 2, s - 2));
		}
		e.fillStyle = this.labelTextColors[n];
	}
	drawBody(e, t, n) {
		let { body: r } = this, { bodySpacing: i, bodyAlign: a, displayColors: o, boxHeight: s, boxWidth: c, boxPadding: l } = n, u = yl(n.bodyFont), d = u.lineHeight, f = 0, p = yu(n.rtl, this.x, this.width), m = function(n) {
			t.fillText(n, p.x(e.x + f), e.y + d / 2), e.y += d + i;
		}, h = p.textAlign(a), g, _, v, y, b, x, S;
		for (t.textAlign = a, t.textBaseline = "middle", t.font = u.string, e.x = Jm(this, h, n), t.fillStyle = n.bodyColor, U(this.beforeBody, m), f = o && h !== "right" ? a === "center" ? c / 2 + l : c + 2 + l : 0, y = 0, x = r.length; y < x; ++y) {
			for (g = r[y], _ = this.labelTextColors[y], t.fillStyle = _, U(g.before, m), v = g.lines, o && v.length && (this._drawColorBox(t, e, y, p, n), d = Math.max(u.lineHeight, s)), b = 0, S = v.length; b < S; ++b) m(v[b]), d = u.lineHeight;
			U(g.after, m);
		}
		f = 0, d = u.lineHeight, U(this.afterBody, m), e.y -= i;
	}
	drawFooter(e, t, n) {
		let r = this.footer, i = r.length, a, o;
		if (i) {
			let s = yu(n.rtl, this.x, this.width);
			for (e.x = Jm(this, n.footerAlign, n), e.y += n.footerMarginTop, t.textAlign = s.textAlign(n.footerAlign), t.textBaseline = "middle", a = yl(n.footerFont), t.fillStyle = n.footerColor, t.font = a.string, o = 0; o < i; ++o) t.fillText(r[o], s.x(e.x), e.y + a.lineHeight / 2), e.y += a.lineHeight + n.footerSpacing;
		}
	}
	drawBackground(e, t, n, r) {
		let { xAlign: i, yAlign: a } = this, { x: o, y: s } = e, { width: c, height: l } = n, { topLeft: u, topRight: d, bottomLeft: f, bottomRight: p } = _l(r.cornerRadius);
		t.fillStyle = r.backgroundColor, t.strokeStyle = r.borderColor, t.lineWidth = r.borderWidth, t.beginPath(), t.moveTo(o + u, s), a === "top" && this.drawCaret(e, t, n, r), t.lineTo(o + c - d, s), t.quadraticCurveTo(o + c, s, o + c, s + d), a === "center" && i === "right" && this.drawCaret(e, t, n, r), t.lineTo(o + c, s + l - p), t.quadraticCurveTo(o + c, s + l, o + c - p, s + l), a === "bottom" && this.drawCaret(e, t, n, r), t.lineTo(o + f, s + l), t.quadraticCurveTo(o, s + l, o, s + l - f), a === "center" && i === "left" && this.drawCaret(e, t, n, r), t.lineTo(o, s + u), t.quadraticCurveTo(o, s, o + u, s), t.closePath(), t.fill(), r.borderWidth > 0 && t.stroke();
	}
	_updateAnimationTarget(e) {
		let t = this.chart, n = this.$animations, r = n && n.x, i = n && n.y;
		if (r || i) {
			let n = Im[e.position].call(this, this._active, this._eventPosition);
			if (!n) return;
			let a = this._size = Bm(this, e), o = Object.assign({}, n, this._size), s = Wm(t, e, o), c = qm(e, o, s, t);
			(r._to !== c.x || i._to !== c.y) && (this.xAlign = s.xAlign, this.yAlign = s.yAlign, this.width = a.width, this.height = a.height, this.caretX = n.x, this.caretY = n.y, this._resolveAnimations().update(this, c));
		}
	}
	_willRender() {
		return !!this.opacity;
	}
	draw(e) {
		let t = this.options.setContext(this.getContext()), n = this.opacity;
		if (!n) return;
		this._updateAnimationTarget(t);
		let r = {
			width: this.width,
			height: this.height
		}, i = {
			x: this.x,
			y: this.y
		};
		n = Math.abs(n) < .001 ? 0 : n;
		let a = vl(t.padding), o = this.title.length || this.beforeBody.length || this.body.length || this.afterBody.length || this.footer.length;
		t.enabled && o && (e.save(), e.globalAlpha = n, this.drawBackground(i, e, r, t), bu(e, t.textDirection), i.y += a.top, this.drawTitle(i, e, t), this.drawBody(i, e, t), this.drawFooter(i, e, t), xu(e, t.textDirection), e.restore());
	}
	getActiveElements() {
		return this._active || [];
	}
	setActiveElements(e, t) {
		let n = this._active, r = e.map(({ datasetIndex: e, index: t }) => {
			let n = this.chart.getDatasetMeta(e);
			if (!n) throw Error("Cannot find a dataset at index " + e);
			return {
				datasetIndex: e,
				element: n.data[t],
				index: t
			};
		}), i = !ws(n, r), a = this._positionChanged(r, t);
		(i || a) && (this._active = r, this._eventPosition = t, this._ignoreReplayEvents = !0, this.update(!0));
	}
	handleEvent(e, t, n = !0) {
		if (t && this._ignoreReplayEvents) return !1;
		this._ignoreReplayEvents = !1;
		let r = this.options, i = this._active || [], a = this._getActiveElements(e, i, t, n), o = this._positionChanged(a, e), s = t || !ws(a, i) || o;
		return s && (this._active = a, (r.enabled || r.external) && (this._eventPosition = {
			x: e.x,
			y: e.y
		}, this.update(!0, t))), s;
	}
	_getActiveElements(e, t, n, r) {
		let i = this.options;
		if (e.type === "mouseout") return [];
		if (!r) return t.filter((e) => this.chart.data.datasets[e.datasetIndex] && this.chart.getDatasetMeta(e.datasetIndex).controller.getParsed(e.index) !== void 0);
		let a = this.chart.getElementsAtEventForMode(e, i.mode, i, n);
		return i.reverse && a.reverse(), a;
	}
	_positionChanged(e, t) {
		let { caretX: n, caretY: r, options: i } = this, a = Im[i.position].call(this, e, t);
		return a !== !1 && (n !== a.x || r !== a.y);
	}
}, th = {
	id: "tooltip",
	_element: eh,
	positioners: Im,
	afterInit(e, t, n) {
		n && (e.tooltip = new eh({
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
		let t = e.tooltip;
		if (t && t._willRender()) {
			let n = { tooltip: t };
			if (e.notifyPlugins("beforeTooltipDraw", {
				...n,
				cancelable: !0
			}) === !1) return;
			t.draw(e.ctx), e.notifyPlugins("afterTooltipDraw", n);
		}
	},
	afterEvent(e, t) {
		if (e.tooltip) {
			let n = t.replay;
			e.tooltip.handleEvent(t.event, n, t.inChartArea) && (t.changed = !0);
		}
	},
	defaults: {
		enabled: !0,
		external: null,
		position: "average",
		backgroundColor: "rgba(0,0,0,0.8)",
		titleColor: "#fff",
		titleFont: { weight: "bold" },
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
		footerFont: { weight: "bold" },
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
		callbacks: Qm
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
		animation: { _fallback: !1 },
		animations: { _fallback: "animation" }
	},
	additionalOptionScopes: ["interaction"]
}, nh = (e, t, n, r) => (typeof t == "string" ? (n = e.push(t) - 1, r.unshift({
	index: n,
	label: t
})) : isNaN(t) && (n = null), n);
function rh(e, t, n, r) {
	let i = e.indexOf(t);
	return i === -1 ? nh(e, t, n, r) : i === e.lastIndexOf(t) ? i : n;
}
var ih = (e, t) => e === null ? null : uc(Math.round(e), 0, t);
function ah(e) {
	let t = this.getLabels();
	return e >= 0 && e < t.length ? t[e] : e;
}
var oh = class extends Wf {
	static id = "category";
	static defaults = { ticks: { callback: ah } };
	constructor(e) {
		super(e), this._startValue = void 0, this._valueRange = 0, this._addedLabels = [];
	}
	init(e) {
		let t = this._addedLabels;
		if (t.length) {
			let e = this.getLabels();
			for (let { index: n, label: r } of t) e[n] === r && e.splice(n, 1);
			this._addedLabels = [];
		}
		super.init(e);
	}
	parse(e, t) {
		if (L(e)) return null;
		let n = this.getLabels();
		return t = isFinite(t) && n[t] === e ? t : rh(n, e, V(t, e), this._addedLabels), ih(t, n.length - 1);
	}
	determineDataLimits() {
		let { minDefined: e, maxDefined: t } = this.getUserBounds(), { min: n, max: r } = this.getMinMax(!0);
		this.options.bounds === "ticks" && (e || (n = 0), t || (r = this.getLabels().length - 1)), this.min = n, this.max = r;
	}
	buildTicks() {
		let e = this.min, t = this.max, n = this.options.offset, r = [], i = this.getLabels();
		i = e === 0 && t === i.length - 1 ? i : i.slice(e, t + 1), this._valueRange = Math.max(i.length - +!n, 1), this._startValue = this.min - (n ? .5 : 0);
		for (let n = e; n <= t; n++) r.push({ value: n });
		return r;
	}
	getLabelForValue(e) {
		return ah.call(this, e);
	}
	configure() {
		super.configure(), this.isHorizontal() || (this._reversePixels = !this._reversePixels);
	}
	getPixelForValue(e) {
		return typeof e != "number" && (e = this.parse(e)), e === null ? NaN : this.getPixelForDecimal((e - this._startValue) / this._valueRange);
	}
	getPixelForTick(e) {
		let t = this.ticks;
		return e < 0 || e > t.length - 1 ? null : this.getPixelForValue(t[e].value);
	}
	getValueForPixel(e) {
		return Math.round(this._startValue + this.getDecimalForPixel(e) * this._valueRange);
	}
	getBasePixel() {
		return this.bottom;
	}
};
function sh(e, t) {
	let n = [], { bounds: r, step: i, min: a, max: o, precision: s, count: c, maxTicks: l, maxDigits: u, includeBounds: d } = e, f = i || 1, p = l - 1, { min: m, max: h } = t, g = !L(a), _ = !L(o), v = !L(c), y = (h - m) / (u + 1), b = Xs((h - m) / p / f) * f, x, S, C, w;
	if (b < 1e-14 && !g && !_) return [{ value: m }, { value: h }];
	w = Math.ceil(h / b) - Math.floor(m / b), w > p && (b = Xs(w * b / p / f) * f), L(s) || (x = 10 ** s, b = Math.ceil(b * x) / x), r === "ticks" ? (S = Math.floor(m / b) * b, C = Math.ceil(h / b) * b) : (S = m, C = h), g && _ && i && ec((o - a) / i, b / 1e3) ? (w = Math.round(Math.min((o - a) / b, l)), b = (o - a) / w, S = a, C = o) : v ? (S = g ? a : S, C = _ ? o : C, w = c - 1, b = (C - S) / w) : (w = (C - S) / b, w = Ys(w, Math.round(w), b / 1e3) ? Math.round(w) : Math.ceil(w));
	let T = Math.max(ic(b), ic(S));
	x = 10 ** (L(s) ? T : s), S = Math.round(S * x) / x, C = Math.round(C * x) / x;
	let E = 0;
	for (g && (d && S !== a ? (n.push({ value: a }), S < a && E++, Ys(Math.round((S + E * b) * x) / x, a, ch(a, y, e)) && E++) : S < a && E++); E < w; ++E) {
		let e = Math.round((S + E * b) * x) / x;
		if (_ && e > o) break;
		n.push({ value: e });
	}
	return _ && d && C !== o ? n.length && Ys(n[n.length - 1].value, o, ch(o, y, e)) ? n[n.length - 1].value = o : n.push({ value: o }) : (!_ || C === o) && n.push({ value: C }), n;
}
function ch(e, t, { horizontal: n, minRotation: r }) {
	let i = nc(r), a = (n ? Math.sin(i) : Math.cos(i)) || .001, o = .75 * t * ("" + e).length;
	return Math.min(t / a, o);
}
var lh = class extends Wf {
	constructor(e) {
		super(e), this.start = void 0, this.end = void 0, this._startValue = void 0, this._endValue = void 0, this._valueRange = 0;
	}
	parse(e, t) {
		return L(e) || (typeof e == "number" || e instanceof Number) && !isFinite(+e) ? null : +e;
	}
	handleTickRangeOptions() {
		let { beginAtZero: e } = this.options, { minDefined: t, maxDefined: n } = this.getUserBounds(), { min: r, max: i } = this, a = (e) => r = t ? r : e, o = (e) => i = n ? i : e;
		if (e) {
			let e = Js(r), t = Js(i);
			e < 0 && t < 0 ? o(0) : e > 0 && t > 0 && a(0);
		}
		if (r === i) {
			let t = i === 0 ? 1 : Math.abs(i * .05);
			o(i + t), e || a(r - t);
		}
		this.min = r, this.max = i;
	}
	getTickLimit() {
		let { maxTicksLimit: e, stepSize: t } = this.options.ticks, n;
		return t ? (n = Math.ceil(this.max / t) - Math.floor(this.min / t) + 1, n > 1e3 && (console.warn(`scales.${this.id}.ticks.stepSize: ${t} would result generating up to ${n} ticks. Limiting to 1000.`), n = 1e3)) : (n = this.computeTickLimit(), e ||= 11), e && (n = Math.min(e, n)), n;
	}
	computeTickLimit() {
		return Infinity;
	}
	buildTicks() {
		let e = this.options, t = e.ticks, n = this.getTickLimit();
		n = Math.max(2, n);
		let r = sh({
			maxTicks: n,
			bounds: e.bounds,
			min: e.min,
			max: e.max,
			precision: t.precision,
			step: t.stepSize,
			count: t.count,
			maxDigits: this._maxDigits(),
			horizontal: this.isHorizontal(),
			minRotation: t.minRotation || 0,
			includeBounds: t.includeBounds !== !1
		}, this._range || this);
		return e.bounds === "ticks" && tc(r, this, "value"), e.reverse ? (r.reverse(), this.start = this.max, this.end = this.min) : (this.start = this.min, this.end = this.max), r;
	}
	configure() {
		let e = this.ticks, t = this.min, n = this.max;
		if (super.configure(), this.options.offset && e.length) {
			let r = (n - t) / Math.max(e.length - 1, 1) / 2;
			t -= r, n += r;
		}
		this._startValue = t, this._endValue = n, this._valueRange = n - t;
	}
	getLabelForValue(e) {
		return zc(e, this.chart.options.locale, this.options.ticks.format);
	}
}, uh = class extends lh {
	static id = "linear";
	static defaults = { ticks: { callback: Hc.formatters.numeric } };
	determineDataLimits() {
		let { min: e, max: t } = this.getMinMax(!0);
		this.min = B(e) ? e : 0, this.max = B(t) ? t : 1, this.handleTickRangeOptions();
	}
	computeTickLimit() {
		let e = this.isHorizontal(), t = e ? this.width : this.height, n = nc(this.options.ticks.minRotation), r = (e ? Math.sin(n) : Math.cos(n)) || .001, i = this._resolveTickFontOptions(0);
		return Math.ceil(t / Math.min(40, i.lineHeight / r));
	}
	getPixelForValue(e) {
		return e === null ? NaN : this.getPixelForDecimal((e - this._startValue) / this._valueRange);
	}
	getValueForPixel(e) {
		return this._startValue + this.getDecimalForPixel(e) * this._valueRange;
	}
}, dh = (e) => Math.floor(qs(e)), fh = (e, t) => 10 ** (dh(e) + t);
function ph(e) {
	return e / 10 ** dh(e) == 1;
}
function mh(e, t, n) {
	let r = 10 ** n, i = Math.floor(e / r);
	return Math.ceil(t / r) - i;
}
function hh(e, t) {
	let n = dh(t - e);
	for (; mh(e, t, n) > 10;) n++;
	for (; mh(e, t, n) < 10;) n--;
	return Math.min(n, dh(e));
}
function gh(e, { min: t, max: n }) {
	t = Ss(e.min, t);
	let r = [], i = dh(t), a = hh(t, n), o = a < 0 ? 10 ** Math.abs(a) : 1, s = 10 ** a, c = i > a ? 10 ** i : 0, l = Math.round((t - c) * o) / o, u = Math.floor((t - c) / s / 10) * s * 10, d = Math.floor((l - u) / 10 ** a), f = Ss(e.min, Math.round((c + u + d * 10 ** a) * o) / o);
	for (; f < n;) r.push({
		value: f,
		major: ph(f),
		significand: d
	}), d >= 10 ? d = d < 15 ? 15 : 20 : d++, d >= 20 && (a++, d = 2, o = a >= 0 ? 1 : o), f = Math.round((c + u + d * 10 ** a) * o) / o;
	let p = Ss(e.max, f);
	return r.push({
		value: p,
		major: ph(p),
		significand: d
	}), r;
}
(class extends Wf {
	static id = "logarithmic";
	static defaults = { ticks: {
		callback: Hc.formatters.logarithmic,
		major: { enabled: !0 }
	} };
	constructor(e) {
		super(e), this.start = void 0, this.end = void 0, this._startValue = void 0, this._valueRange = 0;
	}
	parse(e, t) {
		let n = lh.prototype.parse.apply(this, [e, t]);
		if (n === 0) {
			this._zero = !0;
			return;
		}
		return B(n) && n > 0 ? n : null;
	}
	determineDataLimits() {
		let { min: e, max: t } = this.getMinMax(!0);
		this.min = B(e) ? Math.max(0, e) : null, this.max = B(t) ? Math.max(0, t) : null, this.options.beginAtZero && (this._zero = !0), this._zero && this.min !== this._suggestedMin && !B(this._userMin) && (this.min = e === fh(this.min, 0) ? fh(this.min, -1) : fh(this.min, 0)), this.handleTickRangeOptions();
	}
	handleTickRangeOptions() {
		let { minDefined: e, maxDefined: t } = this.getUserBounds(), n = this.min, r = this.max, i = (t) => n = e ? n : t, a = (e) => r = t ? r : e;
		n === r && (n <= 0 ? (i(1), a(10)) : (i(fh(n, -1)), a(fh(r, 1)))), n <= 0 && i(fh(r, -1)), r <= 0 && a(fh(n, 1)), this.min = n, this.max = r;
	}
	buildTicks() {
		let e = this.options, t = gh({
			min: this._userMin,
			max: this._userMax
		}, this);
		return e.bounds === "ticks" && tc(t, this, "value"), e.reverse ? (t.reverse(), this.start = this.max, this.end = this.min) : (this.start = this.min, this.end = this.max), t;
	}
	getLabelForValue(e) {
		return e === void 0 ? "0" : zc(e, this.chart.options.locale, this.options.ticks.format);
	}
	configure() {
		let e = this.min;
		super.configure(), this._startValue = qs(e), this._valueRange = qs(this.max) - qs(e);
	}
	getPixelForValue(e) {
		return (e === void 0 || e === 0) && (e = this.min), e === null || isNaN(e) ? NaN : this.getPixelForDecimal(e === this.min ? 0 : (qs(e) - this._startValue) / this._valueRange);
	}
	getValueForPixel(e) {
		let t = this.getDecimalForPixel(e);
		return 10 ** (this._startValue + t * this._valueRange);
	}
});
function _h(e) {
	let t = e.ticks;
	if (t.display && e.display) {
		let e = vl(t.backdropPadding);
		return V(t.font && t.font.size, G.font.size) + e.height;
	}
	return 0;
}
function vh(e, t, n) {
	return n = R(n) ? n : [n], {
		w: Xc(e, t.string, n),
		h: n.length * t.lineHeight
	};
}
function yh(e, t, n, r, i) {
	return e === r || e === i ? {
		start: t - n / 2,
		end: t + n / 2
	} : e < r || e > i ? {
		start: t - n,
		end: t
	} : {
		start: t,
		end: t + n
	};
}
function bh(e) {
	let t = {
		l: e.left + e._padding.left,
		r: e.right - e._padding.right,
		t: e.top + e._padding.top,
		b: e.bottom - e._padding.bottom
	}, n = Object.assign({}, t), r = [], i = [], a = e._pointLabels.length, o = e.options.pointLabels, s = o.centerPointLabels ? W / a : 0;
	for (let c = 0; c < a; c++) {
		let a = o.setContext(e.getPointLabelContext(c));
		i[c] = a.padding;
		let l = e.getPointPosition(c, e.drawingArea + i[c], s), u = yl(a.font), d = vh(e.ctx, u, e._pointLabels[c]);
		r[c] = d;
		let f = cc(e.getIndexAngle(c) + s), p = Math.round(rc(f));
		xh(n, t, f, yh(p, l.x, d.w, 0, 180), yh(p, l.y, d.h, 90, 270));
	}
	e.setCenterPoint(t.l - n.l, n.r - t.r, t.t - n.t, n.b - t.b), e._pointLabelItems = wh(e, r, i);
}
function xh(e, t, n, r, i) {
	let a = Math.abs(Math.sin(n)), o = Math.abs(Math.cos(n)), s = 0, c = 0;
	r.start < t.l ? (s = (t.l - r.start) / a, e.l = Math.min(e.l, t.l - s)) : r.end > t.r && (s = (r.end - t.r) / a, e.r = Math.max(e.r, t.r + s)), i.start < t.t ? (c = (t.t - i.start) / o, e.t = Math.min(e.t, t.t - c)) : i.end > t.b && (c = (i.end - t.b) / o, e.b = Math.max(e.b, t.b + c));
}
function Sh(e, t, n) {
	let r = e.drawingArea, { extra: i, additionalAngle: a, padding: o, size: s } = n, c = e.getPointPosition(t, r + i + o, a), l = Math.round(rc(cc(c.angle + Ws))), u = Dh(c.y, s.h, l), d = Th(l), f = Eh(c.x, s.w, d);
	return {
		visible: !0,
		x: c.x,
		y: u,
		textAlign: d,
		left: f,
		top: u,
		right: f + s.w,
		bottom: u + s.h
	};
}
function Ch(e, t) {
	if (!t) return !0;
	let { left: n, top: r, right: i, bottom: a } = e;
	return !(tl({
		x: n,
		y: r
	}, t) || tl({
		x: n,
		y: a
	}, t) || tl({
		x: i,
		y: r
	}, t) || tl({
		x: i,
		y: a
	}, t));
}
function wh(e, t, n) {
	let r = [], i = e._pointLabels.length, a = e.options, { centerPointLabels: o, display: s } = a.pointLabels, c = {
		extra: _h(a) / 2,
		additionalAngle: o ? W / i : 0
	}, l;
	for (let a = 0; a < i; a++) {
		c.padding = n[a], c.size = t[a];
		let i = Sh(e, a, c);
		r.push(i), s === "auto" && (i.visible = Ch(i, l), i.visible && (l = i));
	}
	return r;
}
function Th(e) {
	return e === 0 || e === 180 ? "center" : e < 180 ? "left" : "right";
}
function Eh(e, t, n) {
	return n === "right" ? e -= t : n === "center" && (e -= t / 2), e;
}
function Dh(e, t, n) {
	return n === 90 || n === 270 ? e -= t / 2 : (n > 270 || n < 90) && (e -= t), e;
}
function Oh(e, t, n) {
	let { left: r, top: i, right: a, bottom: o } = n, { backdropColor: s } = t;
	if (!L(s)) {
		let n = _l(t.borderRadius), c = vl(t.backdropPadding);
		e.fillStyle = s;
		let l = r - c.left, u = i - c.top, d = a - r + c.width, f = o - i + c.height;
		Object.values(n).some((e) => e !== 0) ? (e.beginPath(), ul(e, {
			x: l,
			y: u,
			w: d,
			h: f,
			radius: n
		}), e.fill()) : e.fillRect(l, u, d, f);
	}
}
function kh(e, t) {
	let { ctx: n, options: { pointLabels: r } } = e;
	for (let i = t - 1; i >= 0; i--) {
		let t = e._pointLabelItems[i];
		if (!t.visible) continue;
		let a = r.setContext(e.getPointLabelContext(i));
		Oh(n, a, t);
		let o = yl(a.font), { x: s, y: c, textAlign: l } = t;
		ll(n, e._pointLabels[i], s, c + o.lineHeight / 2, o, {
			color: a.color,
			textAlign: l,
			textBaseline: "middle"
		});
	}
}
function Ah(e, t, n, r) {
	let { ctx: i } = e;
	if (n) i.arc(e.xCenter, e.yCenter, t, 0, Bs);
	else {
		let n = e.getPointPosition(0, t);
		i.moveTo(n.x, n.y);
		for (let a = 1; a < r; a++) n = e.getPointPosition(a, t), i.lineTo(n.x, n.y);
	}
}
function jh(e, t, n, r, i) {
	let a = e.ctx, o = t.circular, { color: s, lineWidth: c } = t;
	!o && !r || !s || !c || n < 0 || (a.save(), a.strokeStyle = s, a.lineWidth = c, a.setLineDash(i.dash || []), a.lineDashOffset = i.dashOffset, a.beginPath(), Ah(e, n, o, r), a.closePath(), a.stroke(), a.restore());
}
function Mh(e, t, n) {
	return Sl(e, {
		label: n,
		index: t,
		type: "pointLabel"
	});
}
(class extends lh {
	static id = "radialLinear";
	static defaults = {
		display: !0,
		animate: !0,
		position: "chartArea",
		angleLines: {
			display: !0,
			lineWidth: 1,
			borderDash: [],
			borderDashOffset: 0
		},
		grid: { circular: !1 },
		startAngle: 0,
		ticks: {
			showLabelBackdrop: !0,
			callback: Hc.formatters.numeric
		},
		pointLabels: {
			backdropColor: void 0,
			backdropPadding: 2,
			display: !0,
			font: { size: 10 },
			callback(e) {
				return e;
			},
			padding: 5,
			centerPointLabels: !1
		}
	};
	static defaultRoutes = {
		"angleLines.color": "borderColor",
		"pointLabels.color": "color",
		"ticks.color": "color"
	};
	static descriptors = { angleLines: { _fallback: "grid" } };
	constructor(e) {
		super(e), this.xCenter = void 0, this.yCenter = void 0, this.drawingArea = void 0, this._pointLabels = [], this._pointLabelItems = [];
	}
	setDimensions() {
		let e = this._padding = vl(_h(this.options) / 2), t = this.width = this.maxWidth - e.width, n = this.height = this.maxHeight - e.height;
		this.xCenter = Math.floor(this.left + t / 2 + e.left), this.yCenter = Math.floor(this.top + n / 2 + e.top), this.drawingArea = Math.floor(Math.min(t, n) / 2);
	}
	determineDataLimits() {
		let { min: e, max: t } = this.getMinMax(!1);
		this.min = B(e) && !isNaN(e) ? e : 0, this.max = B(t) && !isNaN(t) ? t : 0, this.handleTickRangeOptions();
	}
	computeTickLimit() {
		return Math.ceil(this.drawingArea / _h(this.options));
	}
	generateTickLabels(e) {
		lh.prototype.generateTickLabels.call(this, e), this._pointLabels = this.getLabels().map((e, t) => {
			let n = H(this.options.pointLabels.callback, [e, t], this);
			return n || n === 0 ? n : "";
		}).filter((e, t) => this.chart.getDataVisibility(t));
	}
	fit() {
		let e = this.options;
		e.display && e.pointLabels.display ? bh(this) : this.setCenterPoint(0, 0, 0, 0);
	}
	setCenterPoint(e, t, n, r) {
		this.xCenter += Math.floor((e - t) / 2), this.yCenter += Math.floor((n - r) / 2), this.drawingArea -= Math.min(this.drawingArea / 2, Math.max(e, t, n, r));
	}
	getIndexAngle(e) {
		let t = Bs / (this._pointLabels.length || 1), n = this.options.startAngle || 0;
		return cc(e * t + nc(n));
	}
	getDistanceFromCenterForValue(e) {
		if (L(e)) return NaN;
		let t = this.drawingArea / (this.max - this.min);
		return this.options.reverse ? (this.max - e) * t : (e - this.min) * t;
	}
	getValueForDistanceFromCenter(e) {
		if (L(e)) return NaN;
		let t = e / (this.drawingArea / (this.max - this.min));
		return this.options.reverse ? this.max - t : this.min + t;
	}
	getPointLabelContext(e) {
		let t = this._pointLabels || [];
		if (e >= 0 && e < t.length) {
			let n = t[e];
			return Mh(this.getContext(), e, n);
		}
	}
	getPointPosition(e, t, n = 0) {
		let r = this.getIndexAngle(e) - Ws + n;
		return {
			x: Math.cos(r) * t + this.xCenter,
			y: Math.sin(r) * t + this.yCenter,
			angle: r
		};
	}
	getPointPositionForValue(e, t) {
		return this.getPointPosition(e, this.getDistanceFromCenterForValue(t));
	}
	getBasePosition(e) {
		return this.getPointPositionForValue(e || 0, this.getBaseValue());
	}
	getPointLabelPosition(e) {
		let { left: t, top: n, right: r, bottom: i } = this._pointLabelItems[e];
		return {
			left: t,
			top: n,
			right: r,
			bottom: i
		};
	}
	drawBackground() {
		let { backgroundColor: e, grid: { circular: t } } = this.options;
		if (e) {
			let n = this.ctx;
			n.save(), n.beginPath(), Ah(this, this.getDistanceFromCenterForValue(this._endValue), t, this._pointLabels.length), n.closePath(), n.fillStyle = e, n.fill(), n.restore();
		}
	}
	drawGrid() {
		let e = this.ctx, t = this.options, { angleLines: n, grid: r, border: i } = t, a = this._pointLabels.length, o, s, c;
		if (t.pointLabels.display && kh(this, a), r.display && this.ticks.forEach((e, t) => {
			if (t !== 0 || t === 0 && this.min < 0) {
				s = this.getDistanceFromCenterForValue(e.value);
				let n = this.getContext(t), o = r.setContext(n), c = i.setContext(n);
				jh(this, o, s, a, c);
			}
		}), n.display) {
			for (e.save(), o = a - 1; o >= 0; o--) {
				let r = n.setContext(this.getPointLabelContext(o)), { color: i, lineWidth: a } = r;
				!a || !i || (e.lineWidth = a, e.strokeStyle = i, e.setLineDash(r.borderDash), e.lineDashOffset = r.borderDashOffset, s = this.getDistanceFromCenterForValue(t.reverse ? this.min : this.max), c = this.getPointPosition(o, s), e.beginPath(), e.moveTo(this.xCenter, this.yCenter), e.lineTo(c.x, c.y), e.stroke());
			}
			e.restore();
		}
	}
	drawBorder() {}
	drawLabels() {
		let e = this.ctx, t = this.options, n = t.ticks;
		if (!n.display) return;
		let r = this.getIndexAngle(0), i, a;
		e.save(), e.translate(this.xCenter, this.yCenter), e.rotate(r), e.textAlign = "center", e.textBaseline = "middle", this.ticks.forEach((r, o) => {
			if (o === 0 && this.min >= 0 && !t.reverse) return;
			let s = n.setContext(this.getContext(o)), c = yl(s.font);
			if (i = this.getDistanceFromCenterForValue(this.ticks[o].value), s.showLabelBackdrop) {
				e.font = c.string, a = e.measureText(r.label).width, e.fillStyle = s.backdropColor;
				let t = vl(s.backdropPadding);
				e.fillRect(-a / 2 - t.left, -i - c.size / 2 - t.top, a + t.width, c.size + t.height);
			}
			ll(e, r.label, 0, -i, c, {
				color: s.color,
				strokeColor: s.textStrokeColor,
				strokeWidth: s.textStrokeWidth
			});
		}), e.restore();
	}
	drawTitle() {}
});
var Nh = {
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
}, Ph = /* #__PURE__ */ Object.keys(Nh);
function Fh(e, t) {
	return e - t;
}
function Ih(e, t) {
	if (L(t)) return null;
	let n = e._adapter, { parser: r, round: i, isoWeekday: a } = e._parseOpts, o = t;
	return typeof r == "function" && (o = r(o)), B(o) || (o = typeof r == "string" ? n.parse(o, r) : n.parse(o)), o === null ? null : (i && (o = i === "week" && ($s(a) || a === !0) ? n.startOf(o, "isoWeek", a) : n.startOf(o, i)), +o);
}
function Lh(e, t, n, r) {
	let i = Ph.length;
	for (let a = Ph.indexOf(e); a < i - 1; ++a) {
		let e = Nh[Ph[a]], i = e.steps ? e.steps : 2 ** 53 - 1;
		if (e.common && Math.ceil((n - t) / (i * e.size)) <= r) return Ph[a];
	}
	return Ph[i - 1];
}
function Rh(e, t, n, r, i) {
	for (let a = Ph.length - 1; a >= Ph.indexOf(n); a--) {
		let n = Ph[a];
		if (Nh[n].common && e._adapter.diff(i, r, n) >= t - 1) return n;
	}
	return Ph[n ? Ph.indexOf(n) : 0];
}
function zh(e) {
	for (let t = Ph.indexOf(e) + 1, n = Ph.length; t < n; ++t) if (Nh[Ph[t]].common) return Ph[t];
}
function Bh(e, t, n) {
	if (!n) e[t] = !0;
	else if (n.length) {
		let { lo: r, hi: i } = pc(n, t), a = n[r] >= t ? n[r] : n[i];
		e[a] = !0;
	}
}
function Vh(e, t, n, r) {
	let i = e._adapter, a = +i.startOf(t[0].value, r), o = t[t.length - 1].value, s, c;
	for (s = a; s <= o; s = +i.add(s, 1, r)) c = n[s], c >= 0 && (t[c].major = !0);
	return t;
}
function Hh(e, t, n) {
	let r = [], i = {}, a = t.length, o, s;
	for (o = 0; o < a; ++o) s = t[o], i[s] = o, r.push({
		value: s,
		major: !1
	});
	return a === 0 || !n ? r : Vh(e, r, i, n);
}
var Uh = class extends Wf {
	static id = "time";
	static defaults = {
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
			major: { enabled: !1 }
		}
	};
	constructor(e) {
		super(e), this._cache = {
			data: [],
			labels: [],
			all: []
		}, this._unit = "day", this._majorUnit = void 0, this._offsets = {}, this._normalized = !1, this._parseOpts = void 0;
	}
	init(e, t = {}) {
		let n = e.time ||= {}, r = this._adapter = new Dd._date(e.adapters.date);
		r.init(t), ks(n.displayFormats, r.formats()), this._parseOpts = {
			parser: n.parser,
			round: n.round,
			isoWeekday: n.isoWeekday
		}, super.init(e), this._normalized = t.normalized;
	}
	parse(e, t) {
		return e === void 0 ? null : Ih(this, e);
	}
	beforeLayout() {
		super.beforeLayout(), this._cache = {
			data: [],
			labels: [],
			all: []
		};
	}
	determineDataLimits() {
		let e = this.options, t = this._adapter, n = e.time.unit || "day", { min: r, max: i, minDefined: a, maxDefined: o } = this.getUserBounds();
		function s(e) {
			!a && !isNaN(e.min) && (r = Math.min(r, e.min)), !o && !isNaN(e.max) && (i = Math.max(i, e.max));
		}
		(!a || !o) && (s(this._getLabelBounds()), (e.bounds !== "ticks" || e.ticks.source !== "labels") && s(this.getMinMax(!1))), r = B(r) && !isNaN(r) ? r : +t.startOf(Date.now(), n), i = B(i) && !isNaN(i) ? i : +t.endOf(Date.now(), n) + 1, this.min = Math.min(r, i - 1), this.max = Math.max(r + 1, i);
	}
	_getLabelBounds() {
		let e = this.getLabelTimestamps(), t = Infinity, n = -Infinity;
		return e.length && (t = e[0], n = e[e.length - 1]), {
			min: t,
			max: n
		};
	}
	buildTicks() {
		let e = this.options, t = e.time, n = e.ticks, r = n.source === "labels" ? this.getLabelTimestamps() : this._generate();
		e.bounds === "ticks" && r.length && (this.min = this._userMin || r[0], this.max = this._userMax || r[r.length - 1]);
		let i = this.min, a = this.max, o = gc(r, i, a);
		return this._unit = t.unit || (n.autoSkip ? Lh(t.minUnit, this.min, this.max, this._getLabelCapacity(i)) : Rh(this, o.length, t.minUnit, this.min, this.max)), this._majorUnit = !n.major.enabled || this._unit === "year" ? void 0 : zh(this._unit), this.initOffsets(r), e.reverse && o.reverse(), Hh(this, o, this._majorUnit);
	}
	afterAutoSkip() {
		this.options.offsetAfterAutoskip && this.initOffsets(this.ticks.map((e) => +e.value));
	}
	initOffsets(e = []) {
		let t = 0, n = 0, r, i;
		this.options.offset && e.length && (r = this.getDecimalForValue(e[0]), t = e.length === 1 ? 1 - r : (this.getDecimalForValue(e[1]) - r) / 2, i = this.getDecimalForValue(e[e.length - 1]), n = e.length === 1 ? i : (i - this.getDecimalForValue(e[e.length - 2])) / 2);
		let a = e.length < 3 ? .5 : .25;
		t = uc(t, 0, a), n = uc(n, 0, a), this._offsets = {
			start: t,
			end: n,
			factor: 1 / (t + 1 + n)
		};
	}
	_generate() {
		let e = this._adapter, t = this.min, n = this.max, r = this.options, i = r.time, a = i.unit || Lh(i.minUnit, t, n, this._getLabelCapacity(t)), o = V(r.ticks.stepSize, 1), s = a === "week" ? i.isoWeekday : !1, c = $s(s) || s === !0, l = {}, u = t, d, f;
		if (c && (u = +e.startOf(u, "isoWeek", s)), u = +e.startOf(u, c ? "day" : a), e.diff(n, t, a) > 1e5 * o) throw Error(t + " and " + n + " are too far apart with stepSize of " + o + " " + a);
		let p = r.ticks.source === "data" && this.getDataTimestamps();
		for (d = u, f = 0; d < n; d = +e.add(d, o, a), f++) Bh(l, d, p);
		return (d === n || r.bounds === "ticks" || f === 1) && Bh(l, d, p), Object.keys(l).sort(Fh).map((e) => +e);
	}
	getLabelForValue(e) {
		let t = this._adapter, n = this.options.time;
		return n.tooltipFormat ? t.format(e, n.tooltipFormat) : t.format(e, n.displayFormats.datetime);
	}
	format(e, t) {
		let n = this.options.time.displayFormats, r = this._unit, i = t || n[r];
		return this._adapter.format(e, i);
	}
	_tickFormatFunction(e, t, n, r) {
		let i = this.options, a = i.ticks.callback;
		if (a) return H(a, [
			e,
			t,
			n
		], this);
		let o = i.time.displayFormats, s = this._unit, c = this._majorUnit, l = s && o[s], u = c && o[c], d = n[t], f = c && u && d && d.major;
		return this._adapter.format(e, r || (f ? u : l));
	}
	generateTickLabels(e) {
		let t, n, r;
		for (t = 0, n = e.length; t < n; ++t) r = e[t], r.label = this._tickFormatFunction(r.value, t, e);
	}
	getDecimalForValue(e) {
		return e === null ? NaN : (e - this.min) / (this.max - this.min);
	}
	getPixelForValue(e) {
		let t = this._offsets, n = this.getDecimalForValue(e);
		return this.getPixelForDecimal((t.start + n) * t.factor);
	}
	getValueForPixel(e) {
		let t = this._offsets, n = this.getDecimalForPixel(e) / t.factor - t.end;
		return this.min + n * (this.max - this.min);
	}
	_getLabelSize(e) {
		let t = this.options.ticks, n = this.ctx.measureText(e).width, r = nc(this.isHorizontal() ? t.maxRotation : t.minRotation), i = Math.cos(r), a = Math.sin(r), o = this._resolveTickFontOptions(0).size;
		return {
			w: n * i + o * a,
			h: n * a + o * i
		};
	}
	_getLabelCapacity(e) {
		let t = this.options.time, n = t.displayFormats, r = n[t.unit] || n.millisecond, i = this._tickFormatFunction(e, 0, Hh(this, [e], this._majorUnit), r), a = this._getLabelSize(i), o = Math.floor(this.isHorizontal() ? this.width / a.w : this.height / a.h) - 1;
		return o > 0 ? o : 1;
	}
	getDataTimestamps() {
		let e = this._cache.data || [], t, n;
		if (e.length) return e;
		let r = this.getMatchingVisibleMetas();
		if (this._normalized && r.length) return this._cache.data = r[0].controller.getAllParsedValues(this);
		for (t = 0, n = r.length; t < n; ++t) e = e.concat(r[t].controller.getAllParsedValues(this));
		return this._cache.data = this.normalize(e);
	}
	getLabelTimestamps() {
		let e = this._cache.labels || [], t, n;
		if (e.length) return e;
		let r = this.getLabels();
		for (t = 0, n = r.length; t < n; ++t) e.push(Ih(this, r[t]));
		return this._cache.labels = this._normalized ? e : this.normalize(e);
	}
	normalize(e) {
		return bc(e.sort(Fh));
	}
};
function Wh(e, t, n) {
	let r = 0, i = e.length - 1, a, o, s, c;
	n ? (t >= e[r].pos && t <= e[i].pos && ({lo: r, hi: i} = mc(e, "pos", t)), {pos: a, time: s} = e[r], {pos: o, time: c} = e[i]) : (t >= e[r].time && t <= e[i].time && ({lo: r, hi: i} = mc(e, "time", t)), {time: a, pos: s} = e[r], {time: o, pos: c} = e[i]);
	let l = o - a;
	return l ? s + (c - s) * (t - a) / l : s;
}
//#endregion
//#region src/utils/global.js
(class extends Uh {
	static id = "timeseries";
	static defaults = Uh.defaults;
	constructor(e) {
		super(e), this._table = [], this._minPos = void 0, this._tableRange = void 0;
	}
	initOffsets() {
		let e = this._getTimestampsForTable(), t = this._table = this.buildLookupTable(e);
		this._minPos = Wh(t, this.min), this._tableRange = Wh(t, this.max) - this._minPos, super.initOffsets(e);
	}
	buildLookupTable(e) {
		let { min: t, max: n } = this, r = [], i = [], a, o, s, c, l;
		for (a = 0, o = e.length; a < o; ++a) c = e[a], c >= t && c <= n && r.push(c);
		if (r.length < 2) return [{
			time: t,
			pos: 0
		}, {
			time: n,
			pos: 1
		}];
		for (a = 0, o = r.length; a < o; ++a) l = r[a + 1], s = r[a - 1], c = r[a], Math.round((l + s) / 2) !== c && i.push({
			time: c,
			pos: a / (o - 1)
		});
		return i;
	}
	_generate() {
		let e = this.min, t = this.max, n = super.getDataTimestamps();
		return (!n.includes(e) || !n.length) && n.splice(0, 0, e), (!n.includes(t) || n.length === 1) && n.push(t), n.sort((e, t) => e - t);
	}
	_getTimestampsForTable() {
		let e = this._cache.all || [];
		if (e.length) return e;
		let t = this.getDataTimestamps(), n = this.getLabelTimestamps();
		return e = t.length && n.length ? this.normalize(t.concat(n)) : t.length ? t : n, e = this._cache.all = e, e;
	}
	getDecimalForValue(e) {
		return (Wh(this._table, e) - this._minPos) / this._tableRange;
	}
	getValueForPixel(e) {
		let t = this._offsets, n = this.getDecimalForPixel(e) / t.factor - t.end;
		return Wh(this._table, n * this._tableRange + this._minPos, !0);
	}
}), Mp.register(th, Fm, uh, oh, Jp);
var Gh = (e) => e.charAt(0).toUpperCase() + e.slice(1), Kh = (e) => e == null || e === "" ? "" : isNaN(e) ? e : Number.isInteger(e) ? parseInt(e).toLocaleString("fr-FR") : parseFloat(e).toLocaleString("fr-FR", { maximumFractionDigits: 2 }), qh = () => {
	Mp.defaults.font.family = "Marianne", Mp.defaults.font.size = 12, Mp.defaults.font.lineHeight = 1.66, Mp.defaults.color = "#6b6b6b", Mp.defaults.borderColor = "#cecece";
}, Jh = { methods: {
	capitalize: Gh,
	formatNumber: Kh
} }, { min: Yh, max: Xh } = Math, Zh = (e, t = 0, n = 1) => Yh(Xh(t, e), n), Qh = (e) => {
	e._clipped = !1, e._unclipped = e.slice(0);
	for (let t = 0; t <= 3; t++) t < 3 ? ((e[t] < 0 || e[t] > 255) && (e._clipped = !0), e[t] = Zh(e[t], 0, 255)) : t === 3 && (e[t] = Zh(e[t], 0, 1));
	return e;
}, $h = {};
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
]) $h[`[object ${e}]`] = e.toLowerCase();
function K(e) {
	return $h[Object.prototype.toString.call(e)] || "object";
}
//#endregion
//#region node_modules/chroma-js/src/utils/unpack.js
var q = (e, t = null) => e.length >= 3 ? Array.prototype.slice.call(e) : K(e[0]) == "object" && t ? t.split("").filter((t) => e[0][t] !== void 0).map((t) => e[0][t]) : e[0].slice(0), eg = (e) => {
	if (e.length < 2) return null;
	let t = e.length - 1;
	return K(e[t]) == "string" ? e[t].toLowerCase() : null;
}, { PI: tg, min: ng, max: rg } = Math, ig = (e) => Math.round(e * 100) / 100, ag = (e) => Math.round(e * 100) / 100, og = tg * 2, sg = tg / 3, cg = tg / 180, lg = 180 / tg;
function ug(e) {
	return [...e.slice(0, 3).reverse(), ...e.slice(3)];
}
//#endregion
//#region node_modules/chroma-js/src/io/input.js
var J = {
	format: {},
	autodetect: []
}, Y = class {
	constructor(...e) {
		let t = this;
		if (K(e[0]) === "object" && e[0].constructor && e[0].constructor === this.constructor) return e[0];
		let n = eg(e), r = !1;
		if (!n) {
			r = !0, J.sorted ||= (J.autodetect = J.autodetect.sort((e, t) => t.p - e.p), !0);
			for (let t of J.autodetect) if (n = t.test(...e), n) break;
		}
		if (J.format[n]) t._rgb = Qh(J.format[n].apply(null, r ? e : e.slice(0, -1)));
		else throw Error("unknown format: " + e);
		t._rgb.length === 3 && t._rgb.push(1);
	}
	toString() {
		return K(this.hex) == "function" ? this.hex() : `[${this._rgb.join(",")}]`;
	}
}, dg = "3.2.0", X = (...e) => new Y(...e);
X.version = dg;
//#endregion
//#region node_modules/chroma-js/src/colors/w3cx11.js
var fg = {
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
}, pg = /^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/, mg = /^#?([A-Fa-f0-9]{8}|[A-Fa-f0-9]{4})$/, hg = (e) => {
	if (e.match(pg)) {
		(e.length === 4 || e.length === 7) && (e = e.substr(1)), e.length === 3 && (e = e.split(""), e = e[0] + e[0] + e[1] + e[1] + e[2] + e[2]);
		let t = parseInt(e, 16);
		return [
			t >> 16,
			t >> 8 & 255,
			t & 255,
			1
		];
	}
	if (e.match(mg)) {
		(e.length === 5 || e.length === 9) && (e = e.substr(1)), e.length === 4 && (e = e.split(""), e = e[0] + e[0] + e[1] + e[1] + e[2] + e[2] + e[3] + e[3]);
		let t = parseInt(e, 16);
		return [
			t >> 24 & 255,
			t >> 16 & 255,
			t >> 8 & 255,
			Math.round((t & 255) / 255 * 100) / 100
		];
	}
	throw Error(`unknown hex color: ${e}`);
}, { round: gg } = Math, _g = (...e) => {
	let [t, n, r, i] = q(e, "rgba"), a = eg(e) || "auto";
	i === void 0 && (i = 1), a === "auto" && (a = i < 1 ? "rgba" : "rgb"), t = gg(t), n = gg(n), r = gg(r);
	let o = "000000" + (t << 16 | n << 8 | r).toString(16);
	o = o.substr(o.length - 6);
	let s = "0" + gg(i * 255).toString(16);
	switch (s = s.substr(s.length - 2), a.toLowerCase()) {
		case "rgba": return `#${o}${s}`;
		case "argb": return `#${s}${o}`;
		default: return `#${o}`;
	}
};
//#endregion
//#region node_modules/chroma-js/src/ops/clipped.js
Y.prototype.name = function() {
	let e = _g(this._rgb, "rgb");
	for (let t of Object.keys(fg)) if (fg[t] === e) return t.toLowerCase();
	return e;
}, J.format.named = (e) => {
	if (e = e.toLowerCase(), fg[e]) return hg(fg[e]);
	throw Error("unknown color name: " + e);
}, J.autodetect.push({
	p: 5,
	test: (e, ...t) => {
		if (!t.length && K(e) === "string" && fg[e.toLowerCase()]) return "named";
	}
}), Y.prototype.alpha = function(e, t = !1) {
	return e !== void 0 && K(e) === "number" ? t ? (this._rgb[3] = e, this) : new Y([
		this._rgb[0],
		this._rgb[1],
		this._rgb[2],
		e
	], "rgb") : this._rgb[3];
}, Y.prototype.clipped = function() {
	return this._rgb._clipped || !1;
};
//#endregion
//#region node_modules/chroma-js/src/io/lab/lab-constants.js
var vg = {
	Kn: 18,
	labWhitePoint: "d65",
	Xn: .95047,
	Yn: 1,
	Zn: 1.08883,
	t0: .137931034,
	t1: .206896552,
	t2: .12841855,
	t3: .008856452,
	kE: 216 / 24389,
	kKE: 8,
	kK: 24389 / 27,
	RefWhiteRGB: {
		X: .95047,
		Y: 1,
		Z: 1.08883
	},
	MtxRGB2XYZ: {
		m00: .4124564390896922,
		m01: .21267285140562253,
		m02: .0193338955823293,
		m10: .357576077643909,
		m11: .715152155287818,
		m12: .11919202588130297,
		m20: .18043748326639894,
		m21: .07217499330655958,
		m22: .9503040785363679
	},
	MtxXYZ2RGB: {
		m00: 3.2404541621141045,
		m01: -.9692660305051868,
		m02: .055643430959114726,
		m10: -1.5371385127977166,
		m11: 1.8760108454466942,
		m12: -.2040259135167538,
		m20: -.498531409556016,
		m21: .041556017530349834,
		m22: 1.0572251882231791
	},
	As: .9414285350000001,
	Bs: 1.040417467,
	Cs: 1.089532651,
	MtxAdaptMa: {
		m00: .8951,
		m01: -.7502,
		m02: .0389,
		m10: .2664,
		m11: 1.7135,
		m12: -.0685,
		m20: -.1614,
		m21: .0367,
		m22: 1.0296
	},
	MtxAdaptMaI: {
		m00: .9869929054667123,
		m01: .43230526972339456,
		m02: -.008528664575177328,
		m10: -.14705425642099013,
		m11: .5183602715367776,
		m12: .04004282165408487,
		m20: .15996265166373125,
		m21: .0492912282128556,
		m22: .9684866957875502
	}
}, yg = new Map([
	["a", [1.0985, .35585]],
	["b", [1.0985, .35585]],
	["c", [.98074, 1.18232]],
	["d50", [.96422, .82521]],
	["d55", [.95682, .92149]],
	["d65", [.95047, 1.08883]],
	["e", [
		1,
		1,
		1
	]],
	["f2", [.99186, .67393]],
	["f7", [.95041, 1.08747]],
	["f11", [1.00962, .6435]],
	["icc", [.96422, .82521]]
]);
function bg(e) {
	let t = yg.get(String(e).toLowerCase());
	if (!t) throw Error("unknown Lab illuminant " + e);
	vg.labWhitePoint = e, vg.Xn = t[0], vg.Zn = t[1];
}
function xg() {
	return vg.labWhitePoint;
}
//#endregion
//#region node_modules/chroma-js/src/io/lab/lab2rgb.js
var Sg = (...e) => {
	e = q(e, "lab");
	let [t, n, r] = e, [i, a, o] = Cg(t, n, r), [s, c, l] = Tg(i, a, o);
	return [
		s,
		c,
		l,
		e.length > 3 ? e[3] : 1
	];
}, Cg = (e, t, n) => {
	let { kE: r, kK: i, kKE: a, Xn: o, Yn: s, Zn: c } = vg, l = (e + 16) / 116, u = .002 * t + l, d = l - .005 * n, f = u * u * u, p = d * d * d, m = f > r ? f : (116 * u - 16) / i, h = e > a ? ((e + 16) / 116) ** 3 : e / i, g = p > r ? p : (116 * d - 16) / i;
	return [
		m * o,
		h * s,
		g * c
	];
}, wg = (e) => {
	let t = Math.sign(e);
	return e = Math.abs(e), (e <= .0031308 ? e * 12.92 : 1.055 * e ** (1 / 2.4) - .055) * t;
}, Tg = (e, t, n) => {
	let { MtxAdaptMa: r, MtxAdaptMaI: i, MtxXYZ2RGB: a, RefWhiteRGB: o, Xn: s, Yn: c, Zn: l } = vg, u = s * r.m00 + c * r.m10 + l * r.m20, d = s * r.m01 + c * r.m11 + l * r.m21, f = s * r.m02 + c * r.m12 + l * r.m22, p = o.X * r.m00 + o.Y * r.m10 + o.Z * r.m20, m = o.X * r.m01 + o.Y * r.m11 + o.Z * r.m21, h = o.X * r.m02 + o.Y * r.m12 + o.Z * r.m22, g = (e * r.m00 + t * r.m10 + n * r.m20) * (p / u), _ = (e * r.m01 + t * r.m11 + n * r.m21) * (m / d), v = (e * r.m02 + t * r.m12 + n * r.m22) * (h / f), y = g * i.m00 + _ * i.m10 + v * i.m20, b = g * i.m01 + _ * i.m11 + v * i.m21, x = g * i.m02 + _ * i.m12 + v * i.m22, S = wg(y * a.m00 + b * a.m10 + x * a.m20), C = wg(y * a.m01 + b * a.m11 + x * a.m21), w = wg(y * a.m02 + b * a.m12 + x * a.m22);
	return [
		S * 255,
		C * 255,
		w * 255
	];
}, Eg = (...e) => {
	let [t, n, r, ...i] = q(e, "rgb"), [a, o, s] = kg(t, n, r), [c, l, u] = Dg(a, o, s);
	return [
		c,
		l,
		u,
		...i.length > 0 && i[0] < 1 ? [i[0]] : []
	];
};
function Dg(e, t, n) {
	let { Xn: r, Yn: i, Zn: a, kE: o, kK: s } = vg, c = e / r, l = t / i, u = n / a, d = c > o ? c ** (1 / 3) : (s * c + 16) / 116, f = l > o ? l ** (1 / 3) : (s * l + 16) / 116, p = u > o ? u ** (1 / 3) : (s * u + 16) / 116;
	return [
		116 * f - 16,
		500 * (d - f),
		200 * (f - p)
	];
}
function Og(e) {
	let t = Math.sign(e);
	return e = Math.abs(e), (e <= .04045 ? e / 12.92 : ((e + .055) / 1.055) ** 2.4) * t;
}
var kg = (e, t, n) => {
	e = Og(e / 255), t = Og(t / 255), n = Og(n / 255);
	let { MtxRGB2XYZ: r, MtxAdaptMa: i, MtxAdaptMaI: a, Xn: o, Yn: s, Zn: c, As: l, Bs: u, Cs: d } = vg, f = e * r.m00 + t * r.m10 + n * r.m20, p = e * r.m01 + t * r.m11 + n * r.m21, m = e * r.m02 + t * r.m12 + n * r.m22, h = o * i.m00 + s * i.m10 + c * i.m20, g = o * i.m01 + s * i.m11 + c * i.m21, _ = o * i.m02 + s * i.m12 + c * i.m22, v = f * i.m00 + p * i.m10 + m * i.m20, y = f * i.m01 + p * i.m11 + m * i.m21, b = f * i.m02 + p * i.m12 + m * i.m22;
	return v *= h / l, y *= g / u, b *= _ / d, f = v * a.m00 + y * a.m10 + b * a.m20, p = v * a.m01 + y * a.m11 + b * a.m21, m = v * a.m02 + y * a.m12 + b * a.m22, [
		f,
		p,
		m
	];
};
//#endregion
//#region node_modules/chroma-js/src/ops/get.js
Y.prototype.lab = function() {
	return Eg(this._rgb);
}, Object.assign(X, {
	lab: (...e) => new Y(...e, "lab"),
	getLabWhitePoint: xg,
	setLabWhitePoint: bg
}), J.format.lab = Sg, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "lab"), K(e) === "array" && e.length === 3) return "lab";
	}
}), Y.prototype.darken = function(e = 1) {
	let t = this, n = t.lab();
	return n[0] -= vg.Kn * e, new Y(n, "lab").alpha(t.alpha(), !0);
}, Y.prototype.brighten = function(e = 1) {
	return this.darken(-e);
}, Y.prototype.darker = Y.prototype.darken, Y.prototype.brighter = Y.prototype.brighten, Y.prototype.get = function(e) {
	let [t, n] = e.split("."), r = this[t]();
	if (n) {
		let e = t.indexOf(n) - (t.substr(0, 2) === "ok" ? 2 : 0);
		if (e > -1) return r[e];
		throw Error(`unknown channel ${n} in mode ${t}`);
	} else return r;
};
//#endregion
//#region node_modules/chroma-js/src/ops/luminance.js
var { pow: Ag } = Math, jg = 1e-7, Mg = 20;
Y.prototype.luminance = function(e, t = "rgb") {
	if (e !== void 0 && K(e) === "number") {
		if (e === 0) return new Y([
			0,
			0,
			0,
			this._rgb[3]
		], "rgb");
		if (e === 1) return new Y([
			255,
			255,
			255,
			this._rgb[3]
		], "rgb");
		let n = this.luminance(), r = Mg, i = (n, a) => {
			let o = n.interpolate(a, .5, t), s = o.luminance();
			return Math.abs(e - s) < jg || !r-- ? o : s > e ? i(n, o) : i(o, a);
		};
		return new Y([...(n > e ? i(new Y([
			0,
			0,
			0
		]), this) : i(this, new Y([
			255,
			255,
			255
		]))).rgb(), this._rgb[3]]);
	}
	return Ng(...this._rgb.slice(0, 3));
};
var Ng = (e, t, n) => (e = Pg(e), t = Pg(t), n = Pg(n), .2126 * e + .7152 * t + .0722 * n), Pg = (e) => (e /= 255, e <= .03928 ? e / 12.92 : Ag((e + .055) / 1.055, 2.4)), Z = {}, Fg = (e, t, n = .5, ...r) => {
	let i = r[0] || "lrgb";
	if (!Z[i] && !r.length && (i = Object.keys(Z)[0]), !Z[i]) throw Error(`interpolation mode ${i} is not defined`);
	return K(e) !== "object" && (e = new Y(e)), K(t) !== "object" && (t = new Y(t)), Z[i](e, t, n).alpha(e.alpha() + n * (t.alpha() - e.alpha()));
};
//#endregion
//#region node_modules/chroma-js/src/ops/premultiply.js
Y.prototype.mix = Y.prototype.interpolate = function(e, t = .5, ...n) {
	return Fg(this, e, t, ...n);
}, Y.prototype.premultiply = function(e = !1) {
	let t = this._rgb, n = t[3];
	return e ? (this._rgb = [
		t[0] * n,
		t[1] * n,
		t[2] * n,
		n
	], this) : new Y([
		t[0] * n,
		t[1] * n,
		t[2] * n,
		n
	], "rgb");
};
//#endregion
//#region node_modules/chroma-js/src/io/lch/lch2lab.js
var { sin: Ig, cos: Lg } = Math, Rg = (...e) => {
	let [t, n, r] = q(e, "lch");
	return isNaN(r) && (r = 0), r *= cg, [
		t,
		Lg(r) * n,
		Ig(r) * n
	];
}, zg = (...e) => {
	e = q(e, "lch");
	let [t, n, r] = e, [i, a, o] = Rg(t, n, r), [s, c, l] = Sg(i, a, o);
	return [
		s,
		c,
		l,
		e.length > 3 ? e[3] : 1
	];
}, Bg = (...e) => zg(...ug(q(e, "hcl"))), { sqrt: Vg, atan2: Hg, round: Ug } = Math, Wg = (...e) => {
	let [t, n, r] = q(e, "lab"), i = Vg(n * n + r * r), a = (Hg(r, n) * lg + 360) % 360;
	return Ug(i * 1e4) === 0 && (a = NaN), [
		t,
		i,
		a
	];
}, Gg = (...e) => {
	let [t, n, r, ...i] = q(e, "rgb"), [a, o, s] = Eg(t, n, r), [c, l, u] = Wg(a, o, s);
	return [
		c,
		l,
		u,
		...i.length > 0 && i[0] < 1 ? [i[0]] : []
	];
};
Y.prototype.lch = function() {
	return Gg(this._rgb);
}, Y.prototype.hcl = function() {
	return ug(Gg(this._rgb));
}, Object.assign(X, {
	lch: (...e) => new Y(...e, "lch"),
	hcl: (...e) => new Y(...e, "hcl")
}), J.format.lch = zg, J.format.hcl = Bg, ["lch", "hcl"].forEach((e) => J.autodetect.push({
	p: 2,
	test: (...t) => {
		if (t = q(t, e), K(t) === "array" && t.length === 3) return e;
	}
})), Y.prototype.saturate = function(e = 1) {
	let t = this, n = t.lch();
	return n[1] += vg.Kn * e, n[1] < 0 && (n[1] = 0), new Y(n, "lch").alpha(t.alpha(), !0);
}, Y.prototype.desaturate = function(e = 1) {
	return this.saturate(-e);
}, Y.prototype.set = function(e, t, n = !1) {
	let [r, i] = e.split("."), a = this[r]();
	if (i) {
		let e = r.indexOf(i) - (r.substr(0, 2) === "ok" ? 2 : 0);
		if (e > -1) {
			if (K(t) == "string") switch (t.charAt(0)) {
				case "+":
					a[e] += +t;
					break;
				case "-":
					a[e] += +t;
					break;
				case "*":
					a[e] *= +t.substr(1);
					break;
				case "/":
					a[e] /= +t.substr(1);
					break;
				default: a[e] = +t;
			}
			else if (K(t) === "number") a[e] = t;
			else throw Error("unsupported value for Color.set");
			let i = new Y(a, r);
			return n ? (this._rgb = i._rgb, this) : i;
		}
		throw Error(`unknown channel ${i} in mode ${r}`);
	} else return a;
}, Y.prototype.tint = function(e = .5, ...t) {
	return Fg(this, "white", e, ...t);
}, Y.prototype.shade = function(e = .5, ...t) {
	return Fg(this, "black", e, ...t);
}, Z.rgb = (e, t, n) => {
	let r = e._rgb, i = t._rgb;
	return new Y(r[0] + n * (i[0] - r[0]), r[1] + n * (i[1] - r[1]), r[2] + n * (i[2] - r[2]), "rgb");
};
//#endregion
//#region node_modules/chroma-js/src/interpolator/lrgb.js
var { sqrt: Kg, pow: qg } = Math;
Z.lrgb = (e, t, n) => {
	let [r, i, a] = e._rgb, [o, s, c] = t._rgb;
	return new Y(Kg(qg(r, 2) * (1 - n) + qg(o, 2) * n), Kg(qg(i, 2) * (1 - n) + qg(s, 2) * n), Kg(qg(a, 2) * (1 - n) + qg(c, 2) * n), "rgb");
}, Z.lab = (e, t, n) => {
	let r = e.lab(), i = t.lab();
	return new Y(r[0] + n * (i[0] - r[0]), r[1] + n * (i[1] - r[1]), r[2] + n * (i[2] - r[2]), "lab");
};
//#endregion
//#region node_modules/chroma-js/src/interpolator/_hsx.js
var Jg = (e, t, n, r) => {
	let i, a;
	r === "hsl" ? (i = e.hsl(), a = t.hsl()) : r === "hsv" ? (i = e.hsv(), a = t.hsv()) : r === "hcg" ? (i = e.hcg(), a = t.hcg()) : r === "hsi" ? (i = e.hsi(), a = t.hsi()) : r === "lch" || r === "hcl" ? (r = "hcl", i = e.hcl(), a = t.hcl()) : r === "oklch" && (i = e.oklch().reverse(), a = t.oklch().reverse());
	let o, s, c, l, u, d;
	(r.substr(0, 1) === "h" || r === "oklch") && ([o, c, u] = i, [s, l, d] = a);
	let f, p, m, h;
	return !isNaN(o) && !isNaN(s) ? (h = s > o && s - o > 180 ? s - (o + 360) : s < o && o - s > 180 ? s + 360 - o : s - o, p = o + n * h) : isNaN(o) ? isNaN(s) ? p = NaN : (p = s, (u == 1 || u == 0) && r != "hsv" && (f = l)) : (p = o, (d == 1 || d == 0) && r != "hsv" && (f = c)), f === void 0 && (f = c + n * (l - c)), m = u + n * (d - u), r === "oklch" ? new Y([
		m,
		f,
		p
	], r) : new Y([
		p,
		f,
		m
	], r);
}, Yg = (e, t, n) => Jg(e, t, n, "lch");
Z.lch = Yg, Z.hcl = Yg;
//#endregion
//#region node_modules/chroma-js/src/io/num/num2rgb.js
var Xg = (e) => {
	if (K(e) == "number" && e >= 0 && e <= 16777215) return [
		e >> 16,
		e >> 8 & 255,
		e & 255,
		1
	];
	throw Error("unknown num color: " + e);
}, Zg = (...e) => {
	let [t, n, r] = q(e, "rgb");
	return (t << 16) + (n << 8) + r;
};
Y.prototype.num = function() {
	return Zg(this._rgb);
}, Object.assign(X, { num: (...e) => new Y(...e, "num") }), J.format.num = Xg, J.autodetect.push({
	p: 5,
	test: (...e) => {
		if (e.length === 1 && K(e[0]) === "number" && e[0] >= 0 && e[0] <= 16777215) return "num";
	}
}), Z.num = (e, t, n) => {
	let r = e.num();
	return new Y(r + n * (t.num() - r), "num");
};
//#endregion
//#region node_modules/chroma-js/src/io/hcg/hcg2rgb.js
var { floor: Qg } = Math, $g = (...e) => {
	e = q(e, "hcg");
	let [t, n, r] = e, i, a, o;
	r *= 255;
	let s = n * 255;
	if (n === 0) i = a = o = r;
	else {
		t === 360 && (t = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 60;
		let e = Qg(t), c = t - e, l = r * (1 - n), u = l + s * (1 - c), d = l + s * c, f = l + s;
		switch (e) {
			case 0:
				[i, a, o] = [
					f,
					d,
					l
				];
				break;
			case 1:
				[i, a, o] = [
					u,
					f,
					l
				];
				break;
			case 2:
				[i, a, o] = [
					l,
					f,
					d
				];
				break;
			case 3:
				[i, a, o] = [
					l,
					u,
					f
				];
				break;
			case 4:
				[i, a, o] = [
					d,
					l,
					f
				];
				break;
			case 5:
				[i, a, o] = [
					f,
					l,
					u
				];
				break;
		}
	}
	return [
		i,
		a,
		o,
		e.length > 3 ? e[3] : 1
	];
}, e_ = (...e) => {
	let [t, n, r] = q(e, "rgb"), i = ng(t, n, r), a = rg(t, n, r), o = a - i, s = o * 100 / 255, c = i / (255 - o) * 100, l;
	return o === 0 ? l = NaN : (t === a && (l = (n - r) / o), n === a && (l = 2 + (r - t) / o), r === a && (l = 4 + (t - n) / o), l *= 60, l < 0 && (l += 360)), [
		l,
		s,
		c
	];
};
Y.prototype.hcg = function() {
	return e_(this._rgb);
}, X.hcg = (...e) => new Y(...e, "hcg"), J.format.hcg = $g, J.autodetect.push({
	p: 1,
	test: (...e) => {
		if (e = q(e, "hcg"), K(e) === "array" && e.length === 3) return "hcg";
	}
}), Z.hcg = (e, t, n) => Jg(e, t, n, "hcg");
//#endregion
//#region node_modules/chroma-js/src/io/hsi/hsi2rgb.js
var { cos: t_ } = Math, n_ = (...e) => {
	e = q(e, "hsi");
	let [t, n, r] = e, i, a, o;
	return isNaN(t) && (t = 0), isNaN(n) && (n = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 360, t < 1 / 3 ? (o = (1 - n) / 3, i = (1 + n * t_(og * t) / t_(sg - og * t)) / 3, a = 1 - (o + i)) : t < 2 / 3 ? (t -= 1 / 3, i = (1 - n) / 3, a = (1 + n * t_(og * t) / t_(sg - og * t)) / 3, o = 1 - (i + a)) : (t -= 2 / 3, a = (1 - n) / 3, o = (1 + n * t_(og * t) / t_(sg - og * t)) / 3, i = 1 - (a + o)), i = Zh(r * i * 3), a = Zh(r * a * 3), o = Zh(r * o * 3), [
		i * 255,
		a * 255,
		o * 255,
		e.length > 3 ? e[3] : 1
	];
}, { min: r_, sqrt: i_, acos: a_ } = Math, o_ = (...e) => {
	let [t, n, r] = q(e, "rgb");
	t /= 255, n /= 255, r /= 255;
	let i, a = r_(t, n, r), o = (t + n + r) / 3, s = o > 0 ? 1 - a / o : 0;
	return s === 0 ? i = NaN : (i = (t - n + (t - r)) / 2, i /= i_((t - n) * (t - n) + (t - r) * (n - r)), i = a_(i), r > n && (i = og - i), i /= og), [
		i * 360,
		s,
		o
	];
};
Y.prototype.hsi = function() {
	return o_(this._rgb);
}, X.hsi = (...e) => new Y(...e, "hsi"), J.format.hsi = n_, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "hsi"), K(e) === "array" && e.length === 3) return "hsi";
	}
}), Z.hsi = (e, t, n) => Jg(e, t, n, "hsi");
//#endregion
//#region node_modules/chroma-js/src/io/hsl/hsl2rgb.js
var s_ = (...e) => {
	e = q(e, "hsl");
	let [t, n, r] = e, i, a, o;
	if (n === 0) i = a = o = r * 255;
	else {
		let e = [
			0,
			0,
			0
		], s = [
			0,
			0,
			0
		], c = r < .5 ? r * (1 + n) : r + n - r * n, l = 2 * r - c, u = t / 360;
		e[0] = u + 1 / 3, e[1] = u, e[2] = u - 1 / 3;
		for (let t = 0; t < 3; t++) e[t] < 0 && (e[t] += 1), e[t] > 1 && --e[t], 6 * e[t] < 1 ? s[t] = l + (c - l) * 6 * e[t] : 2 * e[t] < 1 ? s[t] = c : 3 * e[t] < 2 ? s[t] = l + (c - l) * (2 / 3 - e[t]) * 6 : s[t] = l;
		[i, a, o] = [
			s[0] * 255,
			s[1] * 255,
			s[2] * 255
		];
	}
	return e.length > 3 ? [
		i,
		a,
		o,
		e[3]
	] : [
		i,
		a,
		o,
		1
	];
}, c_ = (...e) => {
	e = q(e, "rgba");
	let [t, n, r] = e;
	t /= 255, n /= 255, r /= 255;
	let i = ng(t, n, r), a = rg(t, n, r), o = (a + i) / 2, s, c;
	return a === i ? (s = 0, c = NaN) : s = o < .5 ? (a - i) / (a + i) : (a - i) / (2 - a - i), t == a ? c = (n - r) / (a - i) : n == a ? c = 2 + (r - t) / (a - i) : r == a && (c = 4 + (t - n) / (a - i)), c *= 60, c < 0 && (c += 360), e.length > 3 && e[3] !== void 0 ? [
		c,
		s,
		o,
		e[3]
	] : [
		c,
		s,
		o
	];
};
Y.prototype.hsl = function() {
	return c_(this._rgb);
}, X.hsl = (...e) => new Y(...e, "hsl"), J.format.hsl = s_, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "hsl"), K(e) === "array" && e.length === 3) return "hsl";
	}
}), Z.hsl = (e, t, n) => Jg(e, t, n, "hsl");
//#endregion
//#region node_modules/chroma-js/src/io/hsv/hsv2rgb.js
var { floor: l_ } = Math, u_ = (...e) => {
	e = q(e, "hsv");
	let [t, n, r] = e, i, a, o;
	if (r *= 255, n === 0) i = a = o = r;
	else {
		t === 360 && (t = 0), t > 360 && (t -= 360), t < 0 && (t += 360), t /= 60;
		let e = l_(t), s = t - e, c = r * (1 - n), l = r * (1 - n * s), u = r * (1 - n * (1 - s));
		switch (e) {
			case 0:
				[i, a, o] = [
					r,
					u,
					c
				];
				break;
			case 1:
				[i, a, o] = [
					l,
					r,
					c
				];
				break;
			case 2:
				[i, a, o] = [
					c,
					r,
					u
				];
				break;
			case 3:
				[i, a, o] = [
					c,
					l,
					r
				];
				break;
			case 4:
				[i, a, o] = [
					u,
					c,
					r
				];
				break;
			case 5:
				[i, a, o] = [
					r,
					c,
					l
				];
				break;
		}
	}
	return [
		i,
		a,
		o,
		e.length > 3 ? e[3] : 1
	];
}, { min: d_, max: f_ } = Math, p_ = (...e) => {
	e = q(e, "rgb");
	let [t, n, r] = e, i = d_(t, n, r), a = f_(t, n, r), o = a - i, s, c, l;
	return l = a / 255, a === 0 ? (s = NaN, c = 0) : (c = o / a, t === a && (s = (n - r) / o), n === a && (s = 2 + (r - t) / o), r === a && (s = 4 + (t - n) / o), s *= 60, s < 0 && (s += 360)), [
		s,
		c,
		l
	];
};
Y.prototype.hsv = function() {
	return p_(this._rgb);
}, X.hsv = (...e) => new Y(...e, "hsv"), J.format.hsv = u_, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "hsv"), K(e) === "array" && e.length === 3) return "hsv";
	}
}), Z.hsv = (e, t, n) => Jg(e, t, n, "hsv");
//#endregion
//#region node_modules/chroma-js/src/utils/multiply-matrices.js
function m_(e, t) {
	let n = e.length;
	Array.isArray(e[0]) || (e = [e]), Array.isArray(t[0]) || (t = t.map((e) => [e]));
	let r = t[0].length, i = t[0].map((e, n) => t.map((e) => e[n])), a = e.map((e) => i.map((t) => Array.isArray(e) ? e.reduce((e, n, r) => e + n * (t[r] || 0), 0) : t.reduce((t, n) => t + n * e, 0)));
	return n === 1 && (a = a[0]), r === 1 ? a.map((e) => e[0]) : a;
}
//#endregion
//#region node_modules/chroma-js/src/io/oklab/oklab2rgb.js
var h_ = (...e) => {
	e = q(e, "lab");
	let [t, n, r, ...i] = e, [a, o, s] = g_([
		t,
		n,
		r
	]), [c, l, u] = Tg(a, o, s);
	return [
		c,
		l,
		u,
		...i.length > 0 && i[0] < 1 ? [i[0]] : []
	];
};
function g_(e) {
	return m_([
		[
			1.2268798758459243,
			-.5578149944602171,
			.2813910456659647
		],
		[
			-.0405757452148008,
			1.112286803280317,
			-.0717110580655164
		],
		[
			-.0763729366746601,
			-.4214933324022432,
			1.5869240198367816
		]
	], m_([
		[
			1,
			.3963377773761749,
			.2158037573099136
		],
		[
			1,
			-.1055613458156586,
			-.0638541728258133
		],
		[
			1,
			-.0894841775298119,
			-1.2914855480194092
		]
	], e).map((e) => e ** 3));
}
//#endregion
//#region node_modules/chroma-js/src/io/oklab/rgb2oklab.js
var __ = (...e) => {
	let [t, n, r, ...i] = q(e, "rgb");
	return [...v_(kg(t, n, r)), ...i.length > 0 && i[0] < 1 ? [i[0]] : []];
};
function v_(e) {
	return m_([
		[
			.210454268309314,
			.7936177747023054,
			-.0040720430116193
		],
		[
			1.9779985324311684,
			-2.42859224204858,
			.450593709617411
		],
		[
			.0259040424655478,
			.7827717124575296,
			-.8086757549230774
		]
	], m_([
		[
			.819022437996703,
			.3619062600528904,
			-.1288737815209879
		],
		[
			.0329836539323885,
			.9292868615863434,
			.0361446663506424
		],
		[
			.0481771893596242,
			.2642395317527308,
			.6335478284694309
		]
	], e).map((e) => Math.cbrt(e)));
}
Y.prototype.oklab = function() {
	return __(this._rgb);
}, Object.assign(X, { oklab: (...e) => new Y(...e, "oklab") }), J.format.oklab = h_, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "oklab"), K(e) === "array" && e.length === 3) return "oklab";
	}
}), Z.oklab = (e, t, n) => {
	let r = e.oklab(), i = t.oklab();
	return new Y(r[0] + n * (i[0] - r[0]), r[1] + n * (i[1] - r[1]), r[2] + n * (i[2] - r[2]), "oklab");
}, Z.oklch = (e, t, n) => Jg(e, t, n, "oklch");
//#endregion
//#region node_modules/chroma-js/src/generator/average.js
var { pow: y_, sqrt: b_, PI: x_, cos: S_, sin: C_, atan2: w_ } = Math, T_ = (e, t = "lrgb", n = null) => {
	let r = e.length;
	n ||= Array.from(Array(r)).map(() => 1);
	let i = r / n.reduce(function(e, t) {
		return e + t;
	});
	if (n.forEach((e, t) => {
		n[t] *= i;
	}), e = e.map((e) => new Y(e)), t === "lrgb") return E_(e, n);
	let a = e.shift(), o = a.get(t), s = [], c = 0, l = 0;
	for (let e = 0; e < o.length; e++) if (o[e] = (o[e] || 0) * n[0], s.push(isNaN(o[e]) ? 0 : n[0]), t.charAt(e) === "h" && !isNaN(o[e])) {
		let t = o[e] / 180 * x_;
		c += S_(t) * n[0], l += C_(t) * n[0];
	}
	let u = a.alpha() * n[0];
	e.forEach((e, r) => {
		let i = e.get(t);
		u += e.alpha() * n[r + 1];
		for (let e = 0; e < o.length; e++) if (!isNaN(i[e])) if (s[e] += n[r + 1], t.charAt(e) === "h") {
			let t = i[e] / 180 * x_;
			c += S_(t) * n[r + 1], l += C_(t) * n[r + 1];
		} else o[e] += i[e] * n[r + 1];
	});
	for (let e = 0; e < o.length; e++) if (t.charAt(e) === "h") {
		let t = w_(l / s[e], c / s[e]) / x_ * 180;
		for (; t < 0;) t += 360;
		for (; t >= 360;) t -= 360;
		o[e] = t;
	} else o[e] = o[e] / s[e];
	return u /= r, new Y(o, t).alpha(u > .99999 ? 1 : u, !0);
}, E_ = (e, t) => {
	let n = e.length, r = [
		0,
		0,
		0,
		0
	];
	for (let i = 0; i < e.length; i++) {
		let a = e[i], o = t[i] / n, s = a._rgb;
		r[0] += y_(s[0], 2) * o, r[1] += y_(s[1], 2) * o, r[2] += y_(s[2], 2) * o, r[3] += s[3] * o;
	}
	return r[0] = b_(r[0]), r[1] = b_(r[1]), r[2] = b_(r[2]), r[3] > .9999999 && (r[3] = 1), new Y(Qh(r));
}, { pow: D_ } = Math;
function O_(e) {
	let t = "rgb", n = X("#ccc"), r = 0, i = [0, 1], a = [0, 1], o = [], s = [0, 0], c = !1, l = [], u = !1, d = 0, f = 1, p = !1, m = {}, h = !0, g = 1, _ = function(e) {
		if (e ||= ["#fff", "#000"], e && K(e) === "string" && X.brewer && X.brewer[e.toLowerCase()] && (e = X.brewer[e.toLowerCase()]), K(e) === "array") {
			e.length === 1 && (e = [e[0], e[0]]), e = e.slice(0);
			for (let t = 0; t < e.length; t++) e[t] = X(e[t]);
			o.length = 0;
			for (let t = 0; t < e.length; t++) o.push(t / (e.length - 1));
		}
		return S(), l = e;
	}, v = function(e) {
		if (c != null) {
			let t = c.length - 1, n = 0;
			for (; n < t && e >= c[n];) n++;
			return n - 1;
		}
		return 0;
	}, y = (e) => e, b = (e) => e, x = function(e, r) {
		let i, a;
		if (r ??= !1, isNaN(e) || e === null) return n;
		a = r ? e : c && c.length > 2 ? v(e) / (c.length - 2) : f === d ? 1 : (e - d) / (f - d), a = b(a), r || (a = y(a)), g !== 1 && (a = D_(a, g)), a = s[0] + a * (1 - s[0] - s[1]), a = Zh(a, 0, 1);
		let u = Math.floor(a * 1e4);
		if (h && m[u]) i = m[u];
		else {
			if (K(l) === "array") for (let e = 0; e < o.length; e++) {
				let n = o[e];
				if (a <= n) {
					i = l[e];
					break;
				}
				if (a >= n && e === o.length - 1) {
					i = l[e];
					break;
				}
				if (a > n && a < o[e + 1]) {
					a = (a - n) / (o[e + 1] - n), i = X.interpolate(l[e], l[e + 1], a, t);
					break;
				}
			}
			else K(l) === "function" && (i = l(a));
			h && (m[u] = i);
		}
		return i;
	};
	var S = () => m = {};
	_(e);
	let C = function(e) {
		let t = X(x(e));
		return u && t[u] ? t[u]() : t;
	};
	return C.classes = function(e) {
		if (e != null) {
			if (K(e) === "array") c = e, i = [e[0], e[e.length - 1]];
			else {
				let t = X.analyze(i);
				c = e === 0 ? [t.min, t.max] : X.limits(t, "e", e);
			}
			return C;
		}
		return c;
	}, C.domain = function(e) {
		if (!arguments.length) return a;
		a = e.slice(0), d = e[0], f = e[e.length - 1], o = [];
		let t = l.length;
		if (e.length === t && d !== f) for (let t of Array.from(e)) o.push((t - d) / (f - d));
		else {
			for (let e = 0; e < t; e++) o.push(e / (t - 1));
			if (e.length > 2) {
				let t = e.map((t, n) => n / (e.length - 1)), n = e.map((e) => (e - d) / (f - d));
				n.every((e, n) => t[n] === e) || (b = (e) => {
					if (e <= 0 || e >= 1) return e;
					let r = 0;
					for (; e >= n[r + 1];) r++;
					let i = (e - n[r]) / (n[r + 1] - n[r]);
					return t[r] + i * (t[r + 1] - t[r]);
				});
			}
		}
		return i = [d, f], C;
	}, C.mode = function(e) {
		return arguments.length ? (t = e, S(), C) : t;
	}, C.range = function(e, t) {
		return _(e, t), C;
	}, C.out = function(e) {
		return u = e, C;
	}, C.spread = function(e) {
		return arguments.length ? (r = e, C) : r;
	}, C.correctLightness = function(e) {
		return e ??= !0, p = e, S(), y = p ? function(e) {
			let t = x(0, !0).lab()[0], n = x(1, !0).lab()[0], r = t > n, i = x(e, !0).lab()[0], a = t + (n - t) * e, o = i - a, s = 0, c = 1, l = 20;
			for (; Math.abs(o) > .01 && l-- > 0;) (function() {
				return r && (o *= -1), o < 0 ? (s = e, e += (c - e) * .5) : (c = e, e += (s - e) * .5), i = x(e, !0).lab()[0], o = i - a;
			})();
			return e;
		} : (e) => e, C;
	}, C.padding = function(e) {
		return e == null ? s : (K(e) === "number" && (e = [e, e]), s = e, C);
	}, C.colors = function(t, n) {
		arguments.length < 2 && (n = "hex");
		let r = [];
		if (arguments.length === 0) r = l.slice(0);
		else if (t === 1) r = [C(.5)];
		else if (t > 1) {
			let e = i[0], n = i[1] - e;
			r = k_(0, t, !1).map((r) => C(e + r / (t - 1) * n));
		} else {
			e = [];
			let t = [];
			if (c && c.length > 2) for (let e = 1, n = c.length, r = 1 <= n; r ? e < n : e > n; r ? e++ : e--) t.push((c[e - 1] + c[e]) * .5);
			else t = i;
			r = t.map((e) => C(e));
		}
		return X[n] && (r = r.map((e) => e[n]())), r;
	}, C.cache = function(e) {
		return e == null ? h : (h = e, C);
	}, C.gamma = function(e) {
		return e == null ? g : (g = e, C);
	}, C.nodata = function(e) {
		return e == null ? n : (n = X(e), C);
	}, C;
}
function k_(e, t, n) {
	let r = [], i = e < t, a = n ? i ? t + 1 : t - 1 : t;
	for (let t = e; i ? t < a : t > a; i ? t++ : t--) r.push(t);
	return r;
}
//#endregion
//#region node_modules/chroma-js/src/generator/bezier.js
var A_ = function(e) {
	let t = [1, 1];
	for (let n = 1; n < e; n++) {
		let e = [1];
		for (let n = 1; n <= t.length; n++) e[n] = (t[n] || 0) + t[n - 1];
		t = e;
	}
	return t;
}, j_ = function(e) {
	let t, n, r, i;
	if (e = e.map((e) => new Y(e)), e.length === 2) [n, r] = e.map((e) => e.lab()), t = function(e) {
		return new Y([
			0,
			1,
			2
		].map((t) => n[t] + e * (r[t] - n[t])), "lab");
	};
	else if (e.length === 3) [n, r, i] = e.map((e) => e.lab()), t = function(e) {
		return new Y([
			0,
			1,
			2
		].map((t) => (1 - e) * (1 - e) * n[t] + 2 * (1 - e) * e * r[t] + e * e * i[t]), "lab");
	};
	else if (e.length === 4) {
		let a;
		[n, r, i, a] = e.map((e) => e.lab()), t = function(e) {
			return new Y([
				0,
				1,
				2
			].map((t) => (1 - e) * (1 - e) * (1 - e) * n[t] + 3 * (1 - e) * (1 - e) * e * r[t] + 3 * (1 - e) * e * e * i[t] + e * e * e * a[t]), "lab");
		};
	} else if (e.length >= 5) {
		let n, r, i;
		n = e.map((e) => e.lab()), i = e.length - 1, r = A_(i), t = function(e) {
			let t = 1 - e;
			return new Y([
				0,
				1,
				2
			].map((a) => n.reduce((n, o, s) => n + r[s] * t ** (i - s) * e ** s * o[a], 0)), "lab");
		};
	} else throw RangeError("No point in running bezier with only one color.");
	return t;
}, M_ = (e) => {
	let t = j_(e);
	return t.scale = () => O_(t), t;
}, { round: N_ } = Math;
Y.prototype.rgb = function(e = !0) {
	return e === !1 ? this._rgb.slice(0, 3) : this._rgb.slice(0, 3).map(N_);
}, Y.prototype.rgba = function(e = !0) {
	return this._rgb.slice(0, 4).map((t, n) => n < 3 ? e === !1 ? t : N_(t) : t);
}, Object.assign(X, { rgb: (...e) => new Y(...e, "rgb") }), J.format.rgb = (...e) => {
	let t = q(e, "rgba");
	return t[3] === void 0 && (t[3] = 1), t;
}, J.autodetect.push({
	p: 3,
	test: (...e) => {
		if (e = q(e, "rgba"), K(e) === "array" && (e.length === 3 || e.length === 4 && K(e[3]) == "number" && e[3] >= 0 && e[3] <= 1)) return "rgb";
	}
});
//#endregion
//#region node_modules/chroma-js/src/generator/blend.js
var P_ = (e, t, n) => {
	if (!P_[n]) throw Error("unknown blend mode " + n);
	return P_[n](e, t);
}, F_ = (e) => (t, n) => {
	let r = X(n).rgb(), i = X(t).rgb();
	return X.rgb(e(r, i));
}, I_ = (e) => (t, n) => {
	let r = [];
	return r[0] = e(t[0], n[0]), r[1] = e(t[1], n[1]), r[2] = e(t[2], n[2]), r;
};
P_.normal = F_(I_((e) => e)), P_.multiply = F_(I_((e, t) => e * t / 255)), P_.screen = F_(I_((e, t) => 255 * (1 - (1 - e / 255) * (1 - t / 255)))), P_.overlay = F_(I_((e, t) => t < 128 ? 2 * e * t / 255 : 255 * (1 - 2 * (1 - e / 255) * (1 - t / 255)))), P_.darken = F_(I_((e, t) => e > t ? t : e)), P_.lighten = F_(I_((e, t) => e > t ? e : t)), P_.dodge = F_(I_((e, t) => e === 255 ? 255 : (e = t / 255 * 255 / (1 - e / 255), e > 255 ? 255 : e))), P_.burn = F_(I_((e, t) => 255 * (1 - (1 - t / 255) / (e / 255))));
//#endregion
//#region node_modules/chroma-js/src/generator/cubehelix.js
var { pow: L_, sin: R_, cos: z_ } = Math;
function B_(e = 300, t = -1.5, n = 1, r = 1, i = [0, 1]) {
	let a = 0, o;
	K(i) === "array" ? o = i[1] - i[0] : (o = 0, i = [i, i]);
	let s = function(s) {
		let c = og * ((e + 120) / 360 + t * s), l = L_(i[0] + o * s, r), u = (a === 0 ? n : n[0] + s * a) * l * (1 - l) / 2, d = z_(c), f = R_(c), p = l + u * (-.14861 * d + 1.78277 * f), m = l + u * (-.29227 * d - .90649 * f), h = l + 1.97294 * d * u;
		return X(Qh([
			p * 255,
			m * 255,
			h * 255,
			1
		]));
	};
	return s.start = function(t) {
		return t == null ? e : (e = t, s);
	}, s.rotations = function(e) {
		return e == null ? t : (t = e, s);
	}, s.gamma = function(e) {
		return e == null ? r : (r = e, s);
	}, s.hue = function(e) {
		return e == null ? n : (n = e, K(n) === "array" ? (a = n[1] - n[0], a === 0 && (n = n[1])) : a = 0, s);
	}, s.lightness = function(e) {
		return e == null ? i : (K(e) === "array" ? (i = e, o = e[1] - e[0]) : (i = [e, e], o = 0), s);
	}, s.scale = () => X.scale(s), s.hue(n), s;
}
//#endregion
//#region node_modules/chroma-js/src/generator/random.js
var V_ = "0123456789abcdef", { floor: H_, random: U_ } = Math, W_ = (e = U_) => {
	let t = "#";
	for (let n = 0; n < 6; n++) t += V_.charAt(H_(e() * 16));
	return new Y(t, "hex");
}, { log: G_, pow: K_, floor: q_, abs: J_ } = Math;
function Y_(e, t = null) {
	let n = {
		min: Number.MAX_VALUE,
		max: Number.MAX_VALUE * -1,
		sum: 0,
		values: [],
		count: 0
	};
	return K(e) === "object" && (e = Object.values(e)), e.forEach((e) => {
		t && K(e) === "object" && (e = e[t]), e != null && !isNaN(e) && (n.values.push(e), n.sum += e, e < n.min && (n.min = e), e > n.max && (n.max = e), n.count += 1);
	}), n.domain = [n.min, n.max], n.limits = (e, t) => X_(n, e, t), n;
}
function X_(e, t = "equal", n = 7) {
	K(e) == "array" && (e = Y_(e));
	let { min: r, max: i } = e, a = e.values.sort((e, t) => e - t);
	if (n === 1) return [r, i];
	let o = [];
	if (t.substr(0, 1) === "c" && (o.push(r), o.push(i)), t.substr(0, 1) === "e") {
		o.push(r);
		for (let e = 1; e < n; e++) o.push(r + e / n * (i - r));
		o.push(i);
	} else if (t.substr(0, 1) === "l") {
		if (r <= 0) throw Error("Logarithmic scales are only possible for values > 0");
		let e = Math.LOG10E * G_(r), t = Math.LOG10E * G_(i);
		o.push(r);
		for (let r = 1; r < n; r++) o.push(K_(10, e + r / n * (t - e)));
		o.push(i);
	} else if (t.substr(0, 1) === "q") {
		o.push(r);
		for (let e = 1; e < n; e++) {
			let t = (a.length - 1) * e / n, r = q_(t);
			if (r === t) o.push(a[r]);
			else {
				let e = t - r;
				o.push(a[r] * (1 - e) + a[r + 1] * e);
			}
		}
		o.push(i);
	} else if (t.substr(0, 1) === "k") {
		let e, t = a.length, s = Array(t), c = Array(n), l = !0, u = 0, d = null;
		d = [], d.push(r);
		for (let e = 1; e < n; e++) d.push(r + e / n * (i - r));
		for (d.push(i); l;) {
			for (let e = 0; e < n; e++) c[e] = 0;
			for (let e = 0; e < t; e++) {
				let t = a[e], r = Number.MAX_VALUE, i;
				for (let a = 0; a < n; a++) {
					let n = J_(d[a] - t);
					n < r && (r = n, i = a), c[i]++, s[e] = i;
				}
			}
			let r = Array(n);
			for (let e = 0; e < n; e++) r[e] = null;
			for (let n = 0; n < t; n++) e = s[n], r[e] === null ? r[e] = a[n] : r[e] += a[n];
			for (let e = 0; e < n; e++) r[e] *= 1 / c[e];
			l = !1;
			for (let e = 0; e < n; e++) if (r[e] !== d[e]) {
				l = !0;
				break;
			}
			d = r, u++, u > 200 && (l = !1);
		}
		let f = {};
		for (let e = 0; e < n; e++) f[e] = [];
		for (let n = 0; n < t; n++) e = s[n], f[e].push(a[n]);
		let p = [];
		for (let e = 0; e < n; e++) p.push(f[e][0]), p.push(f[e][f[e].length - 1]);
		p = p.sort((e, t) => e - t), o.push(p[0]);
		for (let e = 1; e < p.length; e += 2) {
			let t = p[e];
			!isNaN(t) && o.indexOf(t) === -1 && o.push(t);
		}
	}
	return o;
}
//#endregion
//#region node_modules/chroma-js/src/utils/contrast.js
var Z_ = (e, t) => {
	e = new Y(e), t = new Y(t);
	let n = e.luminance(), r = t.luminance();
	return n > r ? (n + .05) / (r + .05) : (r + .05) / (n + .05);
}, Q_ = .027, $_ = 5e-4, ev = .1, tv = 1.14, nv = .022, rv = 1.414, iv = (e, t) => {
	e = new Y(e), t = new Y(t), e.alpha() < 1 && (e = Fg(t, e, e.alpha(), "rgb"));
	let n = av(...e.rgb()), r = av(...t.rgb()), i = n >= nv ? n : n + (nv - n) ** +rv, a = r >= nv ? r : r + (nv - r) ** +rv, o = a ** .56 - i ** .57, s = a ** .65 - i ** .62, c = Math.abs(a - i) < $_ ? 0 : i < a ? o * tv : s * tv;
	return (Math.abs(c) < ev ? 0 : c > 0 ? c - Q_ : c + Q_) * 100;
};
function av(e, t, n) {
	return .2126729 * (e / 255) ** 2.4 + .7151522 * (t / 255) ** 2.4 + .072175 * (n / 255) ** 2.4;
}
//#endregion
//#region node_modules/chroma-js/src/utils/delta-e.js
var { sqrt: ov, pow: Q, min: sv, max: cv, atan2: lv, abs: uv, cos: dv, sin: fv, exp: pv, PI: mv } = Math;
function hv(e, t, n = 1, r = 1, i = 1) {
	var a = function(e) {
		return 360 * e / (2 * mv);
	}, o = function(e) {
		return 2 * mv * e / 360;
	};
	e = new Y(e), t = new Y(t);
	let [s, c, l] = Array.from(e.lab()), [u, d, f] = Array.from(t.lab()), p = (s + u) / 2, m = (ov(Q(c, 2) + Q(l, 2)) + ov(Q(d, 2) + Q(f, 2))) / 2, h = .5 * (1 - ov(Q(m, 7) / (Q(m, 7) + Q(25, 7)))), g = c * (1 + h), _ = d * (1 + h), v = ov(Q(g, 2) + Q(l, 2)), y = ov(Q(_, 2) + Q(f, 2)), b = (v + y) / 2, x = a(lv(l, g)), S = a(lv(f, _)), C = x >= 0 ? x : x + 360, w = S >= 0 ? S : S + 360, T = uv(C - w) > 180 ? (C + w + 360) / 2 : (C + w) / 2, E = 1 - .17 * dv(o(T - 30)) + .24 * dv(o(2 * T)) + .32 * dv(o(3 * T + 6)) - .2 * dv(o(4 * T - 63)), D = w - C;
	D = uv(D) <= 180 ? D : w <= C ? D + 360 : D - 360, D = 2 * ov(v * y) * fv(o(D) / 2);
	let O = u - s, ee = y - v, k = 1 + .015 * Q(p - 50, 2) / ov(20 + Q(p - 50, 2)), te = 1 + .045 * b, ne = 1 + .015 * b * E, re = 30 * pv(-Q((T - 275) / 25, 2)), ie = -(2 * ov(Q(b, 7) / (Q(b, 7) + Q(25, 7)))) * fv(2 * o(re));
	return cv(0, sv(100, ov(Q(O / (n * k), 2) + Q(ee / (r * te), 2) + Q(D / (i * ne), 2) + ie * (ee / (r * te)) * (D / (i * ne)))));
}
//#endregion
//#region node_modules/chroma-js/src/utils/distance.js
function gv(e, t, n = "lab") {
	e = new Y(e), t = new Y(t);
	let r = e.get(n), i = t.get(n), a = 0;
	for (let e in r) {
		let t = (r[e] || 0) - (i[e] || 0);
		a += t * t;
	}
	return Math.sqrt(a);
}
//#endregion
//#region node_modules/chroma-js/src/utils/valid.js
var _v = (...e) => {
	try {
		return new Y(...e), !0;
	} catch {
		return !1;
	}
}, vv = {
	cool() {
		return O_([X.hsl(180, 1, .9), X.hsl(250, .7, .4)]);
	},
	hot() {
		return O_([
			"#000",
			"#f00",
			"#ff0",
			"#fff"
		], [
			0,
			.25,
			.75,
			1
		]).mode("rgb");
	}
}, yv = {
	OrRd: [
		"#fff7ec",
		"#fee8c8",
		"#fdd49e",
		"#fdbb84",
		"#fc8d59",
		"#ef6548",
		"#d7301f",
		"#b30000",
		"#7f0000"
	],
	PuBu: [
		"#fff7fb",
		"#ece7f2",
		"#d0d1e6",
		"#a6bddb",
		"#74a9cf",
		"#3690c0",
		"#0570b0",
		"#045a8d",
		"#023858"
	],
	BuPu: [
		"#f7fcfd",
		"#e0ecf4",
		"#bfd3e6",
		"#9ebcda",
		"#8c96c6",
		"#8c6bb1",
		"#88419d",
		"#810f7c",
		"#4d004b"
	],
	Oranges: [
		"#fff5eb",
		"#fee6ce",
		"#fdd0a2",
		"#fdae6b",
		"#fd8d3c",
		"#f16913",
		"#d94801",
		"#a63603",
		"#7f2704"
	],
	BuGn: [
		"#f7fcfd",
		"#e5f5f9",
		"#ccece6",
		"#99d8c9",
		"#66c2a4",
		"#41ae76",
		"#238b45",
		"#006d2c",
		"#00441b"
	],
	YlOrBr: [
		"#ffffe5",
		"#fff7bc",
		"#fee391",
		"#fec44f",
		"#fe9929",
		"#ec7014",
		"#cc4c02",
		"#993404",
		"#662506"
	],
	YlGn: [
		"#ffffe5",
		"#f7fcb9",
		"#d9f0a3",
		"#addd8e",
		"#78c679",
		"#41ab5d",
		"#238443",
		"#006837",
		"#004529"
	],
	Reds: [
		"#fff5f0",
		"#fee0d2",
		"#fcbba1",
		"#fc9272",
		"#fb6a4a",
		"#ef3b2c",
		"#cb181d",
		"#a50f15",
		"#67000d"
	],
	RdPu: [
		"#fff7f3",
		"#fde0dd",
		"#fcc5c0",
		"#fa9fb5",
		"#f768a1",
		"#dd3497",
		"#ae017e",
		"#7a0177",
		"#49006a"
	],
	Greens: [
		"#f7fcf5",
		"#e5f5e0",
		"#c7e9c0",
		"#a1d99b",
		"#74c476",
		"#41ab5d",
		"#238b45",
		"#006d2c",
		"#00441b"
	],
	YlGnBu: [
		"#ffffd9",
		"#edf8b1",
		"#c7e9b4",
		"#7fcdbb",
		"#41b6c4",
		"#1d91c0",
		"#225ea8",
		"#253494",
		"#081d58"
	],
	Purples: [
		"#fcfbfd",
		"#efedf5",
		"#dadaeb",
		"#bcbddc",
		"#9e9ac8",
		"#807dba",
		"#6a51a3",
		"#54278f",
		"#3f007d"
	],
	GnBu: [
		"#f7fcf0",
		"#e0f3db",
		"#ccebc5",
		"#a8ddb5",
		"#7bccc4",
		"#4eb3d3",
		"#2b8cbe",
		"#0868ac",
		"#084081"
	],
	Greys: [
		"#ffffff",
		"#f0f0f0",
		"#d9d9d9",
		"#bdbdbd",
		"#969696",
		"#737373",
		"#525252",
		"#252525",
		"#000000"
	],
	YlOrRd: [
		"#ffffcc",
		"#ffeda0",
		"#fed976",
		"#feb24c",
		"#fd8d3c",
		"#fc4e2a",
		"#e31a1c",
		"#bd0026",
		"#800026"
	],
	PuRd: [
		"#f7f4f9",
		"#e7e1ef",
		"#d4b9da",
		"#c994c7",
		"#df65b0",
		"#e7298a",
		"#ce1256",
		"#980043",
		"#67001f"
	],
	Blues: [
		"#f7fbff",
		"#deebf7",
		"#c6dbef",
		"#9ecae1",
		"#6baed6",
		"#4292c6",
		"#2171b5",
		"#08519c",
		"#08306b"
	],
	PuBuGn: [
		"#fff7fb",
		"#ece2f0",
		"#d0d1e6",
		"#a6bddb",
		"#67a9cf",
		"#3690c0",
		"#02818a",
		"#016c59",
		"#014636"
	],
	Viridis: [
		"#440154",
		"#482777",
		"#3f4a8a",
		"#31678e",
		"#26838f",
		"#1f9d8a",
		"#6cce5a",
		"#b6de2b",
		"#fee825"
	],
	Spectral: [
		"#9e0142",
		"#d53e4f",
		"#f46d43",
		"#fdae61",
		"#fee08b",
		"#ffffbf",
		"#e6f598",
		"#abdda4",
		"#66c2a5",
		"#3288bd",
		"#5e4fa2"
	],
	RdYlGn: [
		"#a50026",
		"#d73027",
		"#f46d43",
		"#fdae61",
		"#fee08b",
		"#ffffbf",
		"#d9ef8b",
		"#a6d96a",
		"#66bd63",
		"#1a9850",
		"#006837"
	],
	RdBu: [
		"#67001f",
		"#b2182b",
		"#d6604d",
		"#f4a582",
		"#fddbc7",
		"#f7f7f7",
		"#d1e5f0",
		"#92c5de",
		"#4393c3",
		"#2166ac",
		"#053061"
	],
	PiYG: [
		"#8e0152",
		"#c51b7d",
		"#de77ae",
		"#f1b6da",
		"#fde0ef",
		"#f7f7f7",
		"#e6f5d0",
		"#b8e186",
		"#7fbc41",
		"#4d9221",
		"#276419"
	],
	PRGn: [
		"#40004b",
		"#762a83",
		"#9970ab",
		"#c2a5cf",
		"#e7d4e8",
		"#f7f7f7",
		"#d9f0d3",
		"#a6dba0",
		"#5aae61",
		"#1b7837",
		"#00441b"
	],
	RdYlBu: [
		"#a50026",
		"#d73027",
		"#f46d43",
		"#fdae61",
		"#fee090",
		"#ffffbf",
		"#e0f3f8",
		"#abd9e9",
		"#74add1",
		"#4575b4",
		"#313695"
	],
	BrBG: [
		"#543005",
		"#8c510a",
		"#bf812d",
		"#dfc27d",
		"#f6e8c3",
		"#f5f5f5",
		"#c7eae5",
		"#80cdc1",
		"#35978f",
		"#01665e",
		"#003c30"
	],
	RdGy: [
		"#67001f",
		"#b2182b",
		"#d6604d",
		"#f4a582",
		"#fddbc7",
		"#ffffff",
		"#e0e0e0",
		"#bababa",
		"#878787",
		"#4d4d4d",
		"#1a1a1a"
	],
	PuOr: [
		"#7f3b08",
		"#b35806",
		"#e08214",
		"#fdb863",
		"#fee0b6",
		"#f7f7f7",
		"#d8daeb",
		"#b2abd2",
		"#8073ac",
		"#542788",
		"#2d004b"
	],
	Set2: [
		"#66c2a5",
		"#fc8d62",
		"#8da0cb",
		"#e78ac3",
		"#a6d854",
		"#ffd92f",
		"#e5c494",
		"#b3b3b3"
	],
	Accent: [
		"#7fc97f",
		"#beaed4",
		"#fdc086",
		"#ffff99",
		"#386cb0",
		"#f0027f",
		"#bf5b17",
		"#666666"
	],
	Set1: [
		"#e41a1c",
		"#377eb8",
		"#4daf4a",
		"#984ea3",
		"#ff7f00",
		"#ffff33",
		"#a65628",
		"#f781bf",
		"#999999"
	],
	Set3: [
		"#8dd3c7",
		"#ffffb3",
		"#bebada",
		"#fb8072",
		"#80b1d3",
		"#fdb462",
		"#b3de69",
		"#fccde5",
		"#d9d9d9",
		"#bc80bd",
		"#ccebc5",
		"#ffed6f"
	],
	Dark2: [
		"#1b9e77",
		"#d95f02",
		"#7570b3",
		"#e7298a",
		"#66a61e",
		"#e6ab02",
		"#a6761d",
		"#666666"
	],
	Paired: [
		"#a6cee3",
		"#1f78b4",
		"#b2df8a",
		"#33a02c",
		"#fb9a99",
		"#e31a1c",
		"#fdbf6f",
		"#ff7f00",
		"#cab2d6",
		"#6a3d9a",
		"#ffff99",
		"#b15928"
	],
	Pastel2: [
		"#b3e2cd",
		"#fdcdac",
		"#cbd5e8",
		"#f4cae4",
		"#e6f5c9",
		"#fff2ae",
		"#f1e2cc",
		"#cccccc"
	],
	Pastel1: [
		"#fbb4ae",
		"#b3cde3",
		"#ccebc5",
		"#decbe4",
		"#fed9a6",
		"#ffffcc",
		"#e5d8bd",
		"#fddaec",
		"#f2f2f2"
	]
}, bv = Object.keys(yv), xv = new Map(bv.map((e) => [e.toLowerCase(), e])), Sv = typeof Proxy == "function" ? new Proxy(yv, {
	get(e, t) {
		let n = t.toLowerCase();
		if (xv.has(n)) return e[xv.get(n)];
	},
	getOwnPropertyNames() {
		return Object.getOwnPropertyNames(bv);
	}
}) : yv, Cv = (...e) => {
	e = q(e, "cmyk");
	let [t, n, r, i] = e, a = e.length > 4 ? e[4] : 1;
	return i === 1 ? [
		0,
		0,
		0,
		a
	] : [
		t >= 1 ? 0 : 255 * (1 - t) * (1 - i),
		n >= 1 ? 0 : 255 * (1 - n) * (1 - i),
		r >= 1 ? 0 : 255 * (1 - r) * (1 - i),
		a
	];
}, { max: wv } = Math, Tv = (...e) => {
	let [t, n, r] = q(e, "rgb");
	t /= 255, n /= 255, r /= 255;
	let i = 1 - wv(t, wv(n, r)), a = i < 1 ? 1 / (1 - i) : 0;
	return [
		(1 - t - i) * a,
		(1 - n - i) * a,
		(1 - r - i) * a,
		i
	];
};
Y.prototype.cmyk = function() {
	return Tv(this._rgb);
}, Object.assign(X, { cmyk: (...e) => new Y(...e, "cmyk") }), J.format.cmyk = Cv, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "cmyk"), K(e) === "array" && e.length === 4) return "cmyk";
	}
});
//#endregion
//#region node_modules/chroma-js/src/io/css/hsl2css.js
var Ev = (...e) => {
	let t = q(e, "hsla"), n = eg(e) || "lsa";
	return t[0] = ig(t[0] || 0) + "deg", t[1] = ig(t[1] * 100) + "%", t[2] = ig(t[2] * 100) + "%", n === "hsla" || t.length > 3 && t[3] < 1 ? (t[3] = "/ " + (t.length > 3 ? t[3] : 1), n = "hsla") : t.length = 3, `${n.substr(0, 3)}(${t.join(" ")})`;
}, Dv = (...e) => {
	let t = q(e, "lab"), n = eg(e) || "lab";
	return t[0] = ig(t[0]) + "%", t[1] = ig(t[1]), t[2] = ig(t[2]), n === "laba" || t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `lab(${t.join(" ")})`;
}, Ov = (...e) => {
	let t = q(e, "lch"), n = eg(e) || "lab";
	return t[0] = ig(t[0]) + "%", t[1] = ig(t[1]), t[2] = isNaN(t[2]) ? "none" : ig(t[2]) + "deg", n === "lcha" || t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `lch(${t.join(" ")})`;
}, kv = (...e) => {
	let t = q(e, "lab");
	return t[0] = ig(t[0] * 100) + "%", t[1] = ag(t[1]), t[2] = ag(t[2]), t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `oklab(${t.join(" ")})`;
}, Av = (...e) => {
	let [t, n, r, ...i] = q(e, "rgb"), [a, o, s] = __(t, n, r), [c, l, u] = Wg(a, o, s);
	return [
		c,
		l,
		u,
		...i.length > 0 && i[0] < 1 ? [i[0]] : []
	];
}, jv = (...e) => {
	let t = q(e, "lch");
	return t[0] = ig(t[0] * 100) + "%", t[1] = ag(t[1]), t[2] = isNaN(t[2]) ? "none" : ig(t[2]) + "deg", t.length > 3 && t[3] < 1 ? t[3] = "/ " + (t.length > 3 ? t[3] : 1) : t.length = 3, `oklch(${t.join(" ")})`;
}, { round: Mv } = Math, Nv = (...e) => {
	let t = q(e, "rgba"), n = eg(e) || "rgb";
	if (n.substr(0, 3) === "hsl") return Ev(c_(t), n);
	if (n.substr(0, 3) === "lab") {
		let e = xg();
		bg("d50");
		let r = Dv(Eg(t), n);
		return bg(e), r;
	}
	if (n.substr(0, 3) === "lch") {
		let e = xg();
		bg("d50");
		let r = Ov(Gg(t), n);
		return bg(e), r;
	}
	return n.substr(0, 5) === "oklab" ? kv(__(t)) : n.substr(0, 5) === "oklch" ? jv(Av(t)) : (t[0] = Mv(t[0]), t[1] = Mv(t[1]), t[2] = Mv(t[2]), (n === "rgba" || t.length > 3 && t[3] < 1) && (t[3] = "/ " + (t.length > 3 ? t[3] : 1), n = "rgba"), `${n.substr(0, 3)}(${t.slice(0, n === "rgb" ? 3 : 4).join(" ")})`);
}, Pv = (...e) => {
	e = q(e, "lch");
	let [t, n, r, ...i] = e, [a, o, s] = Rg(t, n, r), [c, l, u] = h_(a, o, s);
	return [
		c,
		l,
		u,
		...i.length > 0 && i[0] < 1 ? [i[0]] : []
	];
}, Fv = "((?:-?\\d+)|(?:-?\\d+(?:\\.\\d+)?)%|none)", Iv = "((?:-?(?:\\d+(?:\\.\\d*)?|\\.\\d+)%?)|none)", Lv = "((?:-?(?:\\d+(?:\\.\\d*)?|\\.\\d+)%)|none)", Rv = "\\s*", zv = "\\s+", Bv = "\\s*,\\s*", Vv = "((?:-?(?:\\d+(?:\\.\\d*)?|\\.\\d+)(?:deg)?)|none)", Hv = "\\s*(?:\\/\\s*((?:[01]|[01]?\\.\\d+)|\\d+(?:\\.\\d+)?%))?", Uv = RegExp("^rgba?\\(" + Rv + [
	Fv,
	Fv,
	Fv
].join(zv) + Hv + "\\)$"), Wv = RegExp("^rgb\\(" + Rv + [
	Fv,
	Fv,
	Fv
].join(Bv) + Rv + "\\)$"), Gv = RegExp("^rgba\\(" + Rv + [
	Fv,
	Fv,
	Fv,
	Iv
].join(Bv) + Rv + "\\)$"), Kv = RegExp("^hsla?\\(" + Rv + [
	Vv,
	Lv,
	Lv
].join(zv) + Hv + "\\)$"), qv = RegExp("^hsl?\\(" + Rv + [
	Vv,
	Lv,
	Lv
].join(Bv) + Rv + "\\)$"), Jv = /^hsla\(\s*(-?\d+(?:\.\d+)?),\s*(-?\d+(?:\.\d+)?)%\s*,\s*(-?\d+(?:\.\d+)?)%\s*,\s*([01]|[01]?\.\d+)\)$/, Yv = RegExp("^lab\\(" + Rv + [
	Iv,
	Iv,
	Iv
].join(zv) + Hv + "\\)$"), Xv = RegExp("^lch\\(" + Rv + [
	Iv,
	Iv,
	Vv
].join(zv) + Hv + "\\)$"), Zv = RegExp("^oklab\\(" + Rv + [
	Iv,
	Iv,
	Iv
].join(zv) + Hv + "\\)$"), Qv = RegExp("^oklch\\(" + Rv + [
	Iv,
	Iv,
	Vv
].join(zv) + Hv + "\\)$"), { round: $v } = Math, ey = (e) => e.map((e, t) => t <= 2 ? Zh($v(e), 0, 255) : e), $ = (e, t = 0, n = 100, r = !1) => (typeof e == "string" && e.endsWith("%") && (e = parseFloat(e.substring(0, e.length - 1)) / 100, e = r ? t + (e + 1) * .5 * (n - t) : t + e * (n - t)), +e), ty = (e, t) => e === "none" ? t : e, ny = (e) => {
	if (e = e.toLowerCase().trim(), e === "transparent") return [
		0,
		0,
		0,
		0
	];
	let t;
	if (J.format.named) try {
		return J.format.named(e);
	} catch {}
	if ((t = e.match(Uv)) || (t = e.match(Wv))) {
		let e = t.slice(1, 4);
		for (let t = 0; t < 3; t++) e[t] = +$(ty(e[t], 0), 0, 255);
		e = ey(e);
		let n = t[4] === void 0 ? 1 : +$(t[4], 0, 1);
		return e[3] = n, e;
	}
	if (t = e.match(Gv)) {
		let e = t.slice(1, 5);
		for (let t = 0; t < 4; t++) e[t] = +$(e[t], 0, 255);
		return e;
	}
	if ((t = e.match(Kv)) || (t = e.match(qv))) {
		let e = t.slice(1, 4);
		e[0] = +ty(e[0].replace("deg", ""), 0), e[1] = $(ty(e[1], 0), 0, 100) * .01, e[2] = $(ty(e[2], 0), 0, 100) * .01;
		let n = ey(s_(e));
		return n[3] = t[4] === void 0 ? 1 : +$(t[4], 0, 1), n;
	}
	if (t = e.match(Jv)) {
		let e = t.slice(1, 4);
		e[1] *= .01, e[2] *= .01;
		let n = s_(e);
		for (let e = 0; e < 3; e++) n[e] = $v(n[e]);
		return n[3] = +t[4], n;
	}
	if (t = e.match(Yv)) {
		let e = t.slice(1, 4);
		e[0] = $(ty(e[0], 0), 0, 100), e[1] = $(ty(e[1], 0), -125, 125, !0), e[2] = $(ty(e[2], 0), -125, 125, !0);
		let n = xg();
		bg("d50");
		let r = ey(Sg(e));
		return bg(n), r[3] = t[4] === void 0 ? 1 : +$(t[4], 0, 1), r;
	}
	if (t = e.match(Xv)) {
		let e = t.slice(1, 4);
		e[0] = $(e[0], 0, 100), e[1] = $(ty(e[1], 0), 0, 150, !1), e[2] = +ty(e[2].replace("deg", ""), 0);
		let n = xg();
		bg("d50");
		let r = ey(zg(e));
		return bg(n), r[3] = t[4] === void 0 ? 1 : +$(t[4], 0, 1), r;
	}
	if (t = e.match(Zv)) {
		let e = t.slice(1, 4);
		e[0] = $(ty(e[0], 0), 0, 1), e[1] = $(ty(e[1], 0), -.4, .4, !0), e[2] = $(ty(e[2], 0), -.4, .4, !0);
		let n = ey(h_(e));
		return n[3] = t[4] === void 0 ? 1 : +$(t[4], 0, 1), n;
	}
	if (t = e.match(Qv)) {
		let e = t.slice(1, 4);
		e[0] = $(ty(e[0], 0), 0, 1), e[1] = $(ty(e[1], 0), 0, .4, !1), e[2] = +ty(e[2].replace("deg", ""), 0);
		let n = ey(Pv(e));
		return n[3] = t[4] === void 0 ? 1 : +$(t[4], 0, 1), n;
	}
};
ny.test = (e) => Uv.test(e) || Kv.test(e) || Yv.test(e) || Xv.test(e) || Zv.test(e) || Qv.test(e) || Wv.test(e) || Gv.test(e) || qv.test(e) || Jv.test(e) || e === "transparent", Y.prototype.css = function(e) {
	return Nv(this._rgb, e);
}, X.css = (...e) => new Y(...e, "css"), J.format.css = ny, J.autodetect.push({
	p: 5,
	test: (e, ...t) => {
		if (!t.length && K(e) === "string" && ny.test(e)) return "css";
	}
}), J.format.gl = (...e) => {
	let t = q(e, "rgba");
	return t[0] *= 255, t[1] *= 255, t[2] *= 255, t;
}, X.gl = (...e) => new Y(...e, "gl"), Y.prototype.gl = function() {
	let e = this._rgb;
	return [
		e[0] / 255,
		e[1] / 255,
		e[2] / 255,
		e[3]
	];
}, Y.prototype.hex = function(e) {
	return _g(this._rgb, e);
}, X.hex = (...e) => new Y(...e, "hex"), J.format.hex = hg, J.autodetect.push({
	p: 4,
	test: (e, ...t) => {
		if (!t.length && K(e) === "string" && [
			3,
			4,
			5,
			6,
			7,
			8,
			9
		].indexOf(e.length) >= 0) return "hex";
	}
});
//#endregion
//#region node_modules/chroma-js/src/io/temp/temperature2rgb.js
var { log: ry } = Math, iy = (e) => {
	let t = e / 100, n, r, i;
	return t < 66 ? (n = 255, r = t < 6 ? 0 : -155.25485562709179 - .44596950469579133 * (r = t - 2) + 104.49216199393888 * ry(r), i = t < 20 ? 0 : -254.76935184120902 + .8274096064007395 * (i = t - 10) + 115.67994401066147 * ry(i)) : (n = 351.97690566805693 + .114206453784165 * (n = t - 55) - 40.25366309332127 * ry(n), r = 325.4494125711974 + .07943456536662342 * (r = t - 50) - 28.0852963507957 * ry(r), i = 255), [
		n,
		r,
		i,
		1
	];
}, { round: ay } = Math, oy = (...e) => {
	let t = q(e, "rgb"), n = t[0], r = t[2], i = 1e3, a = 4e4, o;
	for (; a - i > .4;) {
		o = (a + i) * .5;
		let e = iy(o);
		e[2] / e[0] >= r / n ? a = o : i = o;
	}
	return ay(o);
};
//#endregion
//#region node_modules/chroma-js/src/io/temp/index.js
Y.prototype.temp = Y.prototype.kelvin = Y.prototype.temperature = function() {
	return oy(this._rgb);
};
var sy = (...e) => new Y(...e, "temp");
//#endregion
//#region node_modules/chroma-js/index.js
Object.assign(X, {
	temp: sy,
	kelvin: sy,
	temperature: sy
}), J.format.temp = J.format.kelvin = J.format.temperature = iy, Y.prototype.oklch = function() {
	return Av(this._rgb);
}, Object.assign(X, { oklch: (...e) => new Y(...e, "oklch") }), J.format.oklch = Pv, J.autodetect.push({
	p: 2,
	test: (...e) => {
		if (e = q(e, "oklch"), K(e) === "array" && e.length === 3) return "oklch";
	}
}), Object.assign(X, {
	analyze: Y_,
	average: T_,
	bezier: M_,
	blend: P_,
	brewer: Sv,
	Color: Y,
	colors: fg,
	contrast: Z_,
	contrastAPCA: iv,
	cubehelix: B_,
	deltaE: hv,
	distance: gv,
	input: J,
	interpolate: Fg,
	limits: X_,
	mix: Fg,
	random: W_,
	scale: O_,
	scales: vv,
	valid: _v
});
var cy = X, ly = {
	light: {
		"dsfr-chart-colors-01": "#5C68E5",
		"dsfr-chart-colors-02": "#82B5F2",
		"dsfr-chart-colors-03": "#29598F",
		"dsfr-chart-colors-04": "#31A7AE",
		"dsfr-chart-colors-05": "#81EEF5",
		"dsfr-chart-colors-06": "#B478F1",
		"dsfr-chart-colors-07": "#CFB1F5",
		"dsfr-chart-colors-08": "#CECECE",
		"dsfr-chart-colors-09": "#DBDAFF",
		"dsfr-chart-colors-10": "#00005F",
		"dsfr-chart-colors-11": "#298641",
		"dsfr-chart-colors-12": "#79D289",
		"dsfr-chart-colors-13": "#EFB900",
		"dsfr-chart-colors-14": "#FFA373",
		"dsfr-chart-colors-15": "#E91719",
		"dsfr-chart-colors-default": "#5C68E5",
		"dsfr-chart-colors-neutral": "#B1B1B1"
	},
	dark: {
		"dsfr-chart-colors-01": "#5C68E5",
		"dsfr-chart-colors-02": "#699BD6",
		"dsfr-chart-colors-03": "#4878B1",
		"dsfr-chart-colors-04": "#00828A",
		"dsfr-chart-colors-05": "#51C1C8",
		"dsfr-chart-colors-06": "#BC8AF2",
		"dsfr-chart-colors-07": "#CFB1F5",
		"dsfr-chart-colors-08": "#A4A4A4",
		"dsfr-chart-colors-09": "#B8B9FF",
		"dsfr-chart-colors-10": "#3647CA",
		"dsfr-chart-colors-11": "#298641",
		"dsfr-chart-colors-12": "#449D57",
		"dsfr-chart-colors-13": "#AF8800",
		"dsfr-chart-colors-14": "#FFA373",
		"dsfr-chart-colors-15": "#E16834",
		"dsfr-chart-colors-default": "#5C68E5",
		"dsfr-chart-colors-neutral": "#808080"
	}
};
//#endregion
//#region src/utils/colors.js
function uy({ yparse: e = [], tmpColorParse: t = [], highlightIndex: n = [], selectedPalette: r = "" }) {
	let i = [], a = [], o = by(r);
	for (let s = 0; s < e.length; s++) {
		let c = e[s], l = [], u = [];
		if (t[s]) {
			let e = t[s], n = c && c.length ? c.length : 1;
			l = Array(n).fill(e), u = l.map((e) => cy(e).darken(.8).hex());
		} else if (r === "neutral" && n.length > 0 && Array.isArray(c)) {
			let e = c && c.length ? c.length : 1;
			for (let t = 0; t < e; t++) {
				let e = n.includes(t) ? vy() : yy();
				l.push(e), u.push(cy(e).darken(.8).hex());
			}
		} else if (r.startsWith("divergent")) {
			let e = c && c.length ? c.length : 1;
			l = Array(e).fill(o[s % o.length]), u = l.map((e) => cy(e).darken(.8).hex());
		} else if (r === "categorical" || !r) {
			let e = _y(s, o), t = c && c.length ? c.length : 1;
			l = Array(t).fill(e), u = l.map((e) => cy(e).darken(.8).hex());
		} else {
			let t = e.flat(), n = Math.min(...t), r = Math.max(...t), i = cy.scale(o).domain([r, n]);
			l = (c || [n]).map((e) => cy(i(e)).hex()), u = l.map((e) => cy(e).darken(.8).hex());
		}
		i.push(l), a.push(u);
	}
	return {
		colorParse: i,
		colorHover: a,
		legendColors: i.map((e) => e[0])
	};
}
function dy() {
	return ly[document.documentElement.getAttribute("data-fr-theme") || "light"] || ly.light;
}
function fy() {
	let e = dy();
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
function py() {
	let e = dy();
	return cy.scale([e["dsfr-chart-colors-09"], e["dsfr-chart-colors-10"]]).colors(10);
}
function my() {
	let e = dy();
	return cy.scale([e["dsfr-chart-colors-10"], e["dsfr-chart-colors-09"]]).colors(10);
}
function hy() {
	let e = dy();
	return cy.scale([
		e["dsfr-chart-colors-11"],
		e["dsfr-chart-colors-13"],
		e["dsfr-chart-colors-15"]
	]).colors(4);
}
function gy() {
	let e = dy();
	return cy.scale([
		e["dsfr-chart-colors-15"],
		e["dsfr-chart-colors-13"],
		e["dsfr-chart-colors-11"]
	]).colors(4);
}
function _y(e, t = fy()) {
	return t[e % t.length];
}
function vy() {
	return dy()["dsfr-chart-colors-default"];
}
function yy() {
	return dy()["dsfr-chart-colors-neutral"];
}
function by(e) {
	switch (e) {
		case "default": return [vy()];
		case "neutral": return [yy()];
		case "categorical": return fy();
		case "sequentialAscending": return py();
		case "sequentialDescending": return my();
		case "divergentAscending": return hy();
		case "divergentDescending": return gy();
		default: return fy();
	}
}
//#endregion
//#region \0plugin-vue:export-helper
var xy = (e, t) => {
	let n = e.__vccOpts || e;
	for (let [e, r] of t) n[e] = r;
	return n;
};
//#endregion
//#region src/components/BarChart.vue
Mp.register(Td, im);
var Sy = {
	name: "BarChart",
	mixins: [Jh],
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
		subX: {
			type: String,
			default: null
		},
		subY: {
			type: String,
			default: null
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
			type: [Array, String],
			default: () => []
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
			selectedIndex: -1,
			datasets: [],
			labels: [],
			xparse: [],
			yparse: [],
			subXParse: [],
			subYParse: [],
			nameParse: [],
			tmpColorParse: [],
			colorParse: [],
			colorHover: [],
			legendColors: [],
			isSubChart: !1,
			isSubLevel: !1,
			subTitle: null,
			targetReady: !1
		};
	},
	watch: {
		$props: {
			handler() {
				this.chartId && (this.resetData(), this.getData(), this.createChart());
			},
			deep: !0,
			immediate: !0
		},
		targetReady(e) {
			e && this.$nextTick(() => {
				this.resetData(), this.createChart();
			});
		}
	},
	created() {
		qh(), this.chartId = `dsfr-chart-${Math.floor(Math.random() * 1e3)}`, this.widgetId = `dsfr-widget-${Math.floor(Math.random() * 1e3)}`;
	},
	mounted() {
		if (!this.databoxId || !this.databoxType) this.resetData(), this.createChart();
		else {
			let e = `${this.databoxId}-${this.databoxType}-${this.databoxSource}`;
			document.getElementById(e) ? this.targetReady = !0 : (this._targetObserver = new MutationObserver(() => {
				document.getElementById(e) && (this._targetObserver.disconnect(), this.targetReady = !0);
			}), this._targetObserver.observe(document.body, {
				childList: !0,
				subtree: !0
			}));
		}
		document.documentElement.addEventListener("dsfr.theme", (e) => {
			this.chartId !== "" && this.changeColors(e.detail.theme);
		});
	},
	beforeUnmount() {
		this._targetObserver && this._targetObserver.disconnect();
	},
	methods: {
		resetData() {
			this.chart && this.chart.destroy(), this.datasets = [], this.labels = [], this.xparse = [], this.yparse = [], this.subXParse = [], this.subYParse = [], this.nameParse = [], this.tmpColorParse = [], this.highlightIndexParse = [], this.colorParse = [], this.colorHover = [];
		},
		getData() {
			try {
				this.xparse = JSON.parse(this.x), this.yparse = JSON.parse(this.y), this.subXParse = JSON.parse(this.subX), this.subYParse = JSON.parse(this.subY);
			} catch (e) {
				console.error("Erreur lors du parsing des données x ou y:", e);
				return;
			}
			this.subXParse && this.subYParse && (this.isSubChart = !0);
			let e = [];
			if (this.name) try {
				e = JSON.parse(this.name);
			} catch (e) {
				console.error("Erreur lors du parsing de name:", e);
			}
			this.nameParse = [];
			for (let t = 0; t < this.yparse.length; t++) e[t] ? this.nameParse.push(e[t]) : this.nameParse.push(`Série ${t + 1}`);
			this.labels = this.xparse[0], this.loadColors(), this.datasets = this.yparse.map((e, t) => ({
				data: e,
				borderColor: this.colorParse[t],
				backgroundColor: this.colorParse[t],
				hoverBorderColor: this.colorHover[t],
				hoverBackgroundColor: this.colorHover[t],
				barThickness: this.barSize,
				...this.maxBarSize ? { maxBarThickness: this.maxBarSize } : {}
			}));
		},
		choosePalette() {
			return by(this.selectedPalette);
		},
		loadColors() {
			try {
				this.highlightIndexParse = Array.isArray(this.highlightIndex) ? this.highlightIndex : JSON.parse(this.highlightIndex);
			} catch (e) {
				console.error("Erreur lors du parsing des données highlight-index:", e), this.highlightIndexParse = [];
			}
			let { colorParse: e, colorHover: t, legendColors: n } = uy({
				yparse: this.yparse,
				tmpColorParse: this.tmpColorParse,
				highlightIndex: this.highlightIndexParse,
				selectedPalette: this.selectedPalette
			});
			this.colorParse = e, this.colorHover = t, this.legendColors = n;
		},
		createChart() {
			this.chart && this.chart.destroy(), this.getData();
			let e = this.$refs[this.chartId].getContext("2d");
			this.chart = new Mp(e, {
				type: "bar",
				data: {
					labels: this.labels,
					datasets: this.datasets
				},
				options: {
					indexAxis: [
						!0,
						"true",
						""
					].includes(this.horizontal) ? "y" : "x",
					aspectRatio: this.aspectRatio,
					scales: {
						x: {
							offset: ![
								!0,
								"true",
								""
							].includes(this.horizontal),
							stacked: [
								!0,
								"true",
								""
							].includes(this.stacked),
							grid: {
								drawTicks: !1,
								drawOnChartArea: [
									!0,
									"true",
									""
								].includes(this.horizontal)
							},
							ticks: { padding: [
								!0,
								"true",
								""
							].includes(this.horizontal) ? 5 : 15 },
							...this.xMin ? { suggestedMin: this.xMin } : {},
							...this.xMax ? { suggestedMax: this.xMax } : {}
						},
						y: {
							stacked: [
								!0,
								"true",
								""
							].includes(this.stacked),
							offset: [
								!0,
								"true",
								""
							].includes(this.horizontal),
							grid: {
								drawTicks: !1,
								drawOnChartArea: ![
									!0,
									"true",
									""
								].includes(this.horizontal)
							},
							border: { dash: [3] },
							ticks: {
								autoSkip: !1,
								padding: 5
							},
							...this.yMin ? { suggestedMin: this.yMin } : {},
							...this.yMax ? { suggestedMax: this.yMax } : {}
						}
					},
					plugins: {
						legend: { display: !1 },
						tooltip: {
							enabled: !1,
							mode: "index",
							displayColors: !1,
							backgroundColor: "#6b6b6b",
							callbacks: {
								label: (e) => this.datasets.map((t) => this.formatNumber(t.data[e.dataIndex])),
								title: (e) => e[0].label,
								labelTextColor: () => this.colorParse
							},
							external: (e) => {
								let t = (document.getElementById(`${this.databoxId}-${this.databoxType}-${this.databoxSource}`) || this.$el.nextElementSibling).querySelector(".tooltip"), n = e.tooltip;
								if (!t) return;
								if (!n || n.opacity === 0) {
									t.style.opacity = 0;
									return;
								}
								if (t.classList.remove("above", "below", "no-transform"), n.yAlign ? t.classList.add(n.yAlign) : t.classList.add("no-transform"), n.body) {
									let e = n.title || [], r = [n.body.map((e) => e.lines).flat()], i = t.querySelector(".tooltip_header.fr-text--sm.fr-mb-0");
									i.innerText = e[0];
									let a = t.querySelector(".tooltip_value");
									a.innerHTML = "", r[0].forEach((e, t) => {
										if (e && e !== "NaN" && n.dataPoints[t]) {
											let { datasetIndex: r, dataIndex: i } = n.dataPoints[t], o = this.colorParse[r] ? this.colorParse[r][i] : "#000", s = `${e}${this.unitTooltip ? ` ${this.unitTooltip}` : ""}`;
											a.innerHTML += `
                        <div class="tooltip_value-content">
                          <span class="tooltip_dot" data-color="${o}"></span>
                          <p class="tooltip_place fr-mb-0">${s}</p>
                        </div>
                      `, a.querySelectorAll(".tooltip_dot").forEach((e) => {
												e.style.backgroundColor = e.getAttribute("data-color");
											});
										}
									});
								}
								let { offsetLeft: r, offsetTop: i } = this.chart.canvas, a = Number(this.chart.canvas.style.width.replace(/\D/g, "")), o = Number(this.chart.canvas.style.height.replace(/\D/g, "")), s = r + n.caretX + 10, c = i + n.caretY - 20;
								s + t.clientWidth > r + a && (s = r + n.caretX - t.clientWidth - 10), c + t.clientHeight > i + .9 * o && (c = i + n.caretY - t.clientHeight + 20), s < r && (s = r + n.caretX - t.clientWidth / 2, c = i + n.caretY - t.clientHeight - 20), t.style.position = "absolute", t.style.padding = `${n.padding}px ${n.padding}px`, t.style.pointerEvents = "none", t.style.left = `${s}px`, t.style.top = `${c}px`, t.style.opacity = 1;
							}
						}
					},
					onClick: (e) => {
						if (!this.subYParse) return;
						let t = this.chart.getElementsAtEventForMode(e, "nearest", { intersect: !0 }, !0);
						if (t.length > 0) {
							let { index: e } = t[0], n = this.chart.data.labels[e];
							if (!this.subYParse[e]) return;
							this.subTitle ||= n, this.subYParse[e] && !this.isSubLevel && (this.updateChart(e), this.isSubLevel = !0, this.selectedIndex = e);
						}
					}
				}
			});
		},
		changeColors(e) {
			this.loadColors(), this.chart.data.datasets.forEach((e, t) => {
				e.borderColor = this.colorParse[t], e.backgroundColor = this.colorParse[t], e.hoverBorderColor = this.colorHover[t], e.hoverBackgroundColor = this.colorHover[t];
			}), this.chart.options.scales.x.ticks.color = e === "dark" ? "#cecece" : Mp.defaults.color, this.chart.options.scales.y.ticks.color = e === "dark" ? "#cecece" : Mp.defaults.color, this.chart.update("none");
		},
		updateChart(e) {
			let t = this.subYParse[e];
			!t || t.length === 0 || (this.chart.data.labels = this.subXParse[e], this.chart.data.datasets[0].data = this.subYParse[e], this.chart.update());
		},
		resetSub() {
			this.isSubLevel = !1, this.subTitle = null, this.chart.data.labels = this.xparse[0], this.chart.data.datasets[0].data = this.yparse[0], this.chart.update(), this.selectedIndex = -1;
		}
	}
}, Cy = ["data-index", "data-sub-chart"], wy = { class: "fr-col-12" }, Ty = { class: "chart" }, Ey = {
	key: 1,
	class: "fr-mb-0"
}, Dy = ["aria-labelledby", "aria-label"], Oy = { class: "chart_legend fr-mb-0 fr-mt-4v" }, ky = { class: "fr-text--sm fr-text--bold fr-ml-1w fr-mb-0" }, Ay = {
	key: 1,
	class: "flex fr-mt-1w"
}, jy = { class: "fr-text--xs" };
function My(e, t, n, r, i, a) {
	return !n.databoxId || i.targetReady ? (Hi(), Ji(qn, {
		key: 0,
		to: "#" + n.databoxId + "-" + n.databoxType + "-" + n.databoxSource,
		disabled: !n.databoxId
	}, [$i("div", {
		ref: i.widgetId,
		class: "widget_container fr-grid-row",
		"data-index": i.selectedIndex,
		"data-sub-chart": i.isSubChart
	}, [$i("div", wy, [$i("div", Ty, [
		t[1] ||= $i("div", { class: "tooltip" }, [$i("div", { class: "tooltip_header fr-text--sm fr-mb-0" }), $i("div", { class: "tooltip_body" }, [$i("div", { class: "tooltip_value" })])], -1),
		i.isSubChart ? (Hi(), qi("div", {
			key: 0,
			class: me(i.isSubLevel ? "" : "fr-mt-6v"),
			style: {
				textAlign: "center",
				position: "relative"
			}
		}, [i.isSubLevel ? (Hi(), qi("button", {
			key: 0,
			class: "fr-btn fr-btn--sm fr-icon-arrow-go-back-fill fr-btn--icon-left fr-btn--tertiary-no-outline fr-ml-4w",
			style: {
				position: "absolute",
				left: 0
			},
			onClick: t[0] ||= (...e) => a.resetSub && a.resetSub(...e)
		}, " Retour ")) : aa("", !0), i.subTitle ? (Hi(), qi("p", Ey, xe(i.subTitle), 1)) : aa("", !0)], 2)) : aa("", !0),
		$i("canvas", {
			ref: i.chartId,
			role: "img",
			"aria-labelledby": n.databoxId ? "title-" + n.databoxId : null,
			"aria-label": n.databoxId ? null : "Graphique en barres"
		}, null, 8, Dy),
		$i("div", Oy, [(Hi(!0), qi(Ii, null, Cr(i.nameParse, (t, n) => (Hi(), qi("div", {
			key: n,
			class: "flex fr-mt-3v fr-mb-1v"
		}, [$i("span", {
			class: "legend_dot",
			style: le({ "background-color": i.legendColors[n] })
		}, null, 4), $i("p", ky, xe(e.capitalize(t)), 1)]))), 128))]),
		n.date ? (Hi(), qi("div", Ay, [$i("p", jy, "Mise à jour : " + xe(n.date), 1)])) : aa("", !0)
	])])], 8, Cy)], 8, ["to", "disabled"])) : aa("", !0);
}
//#endregion
//#region src/charts/BarChart.js
var Ny = /* @__PURE__ */ yo(/* @__PURE__ */ xy(Sy, [["render", My]]), { shadowRoot: !1 });
customElements.define("bar-chart", Ny);
//#endregion
