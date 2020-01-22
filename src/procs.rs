use crate::pmf::PMF;

const M: i32 = 20;

fn subs(v: &Vec<f64>, x: f64) -> f64 {
    let mut sum = 0.0;
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            sum += coef * (x).powf(idx as f64);
        }
    }
    return sum;
}

fn print(name: String, v: &Vec<f64>) {
    let mut dist = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if coef > &0.0 {
            let string = format!("{:.4}x^{{{}}}", coef, idx);
            dist.push(string);
        }
    }
    let dist = dist.join("+");
    println!("{}={}", name, dist);
}

fn deriv(v: &[f64]) -> Vec<f64> {
    let mut ret: Vec<f64> = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        if idx > 0 {
            ret.push(*coef * idx as f64);
        }
    }
    return ret;
}

fn binom(n: i32, k: i32) -> i32 {
    // (c) Knuth
    (0..n + 1).rev().zip(1..k + 1).fold(1, |mut r, (n, d)| {
        r *= n;
        r /= d;
        r
    })
}

fn mul(v: &Vec<f64>, m: &f64) -> Vec<f64> {
    let mut ret: Vec<f64> = Vec::new();
    for (idx, coef) in v.iter().enumerate() {
        ret.push(*coef * m);
    }
    return ret;
}

#[allow(non_snake_case)]
pub fn run() {
    let Lx = PMF.to_vec();
    let L1 = subs(&deriv(&Lx), 1.0);
    let lx = mul(&deriv(&Lx), &(1.0 / L1));
    print("L(x)".to_string(), &Lx);
    print("l(x)".to_string(), &lx);
    let tmax = 0.0;
    // for i in (0..2) {
    //     let g = (i as f64) * 0.0001;
    //     let lmbd = g * L1;
    //     let mut Rx = Vec::new();
    //     for k in (0..M) {
    //         let s = lmbd.powf(k as f64) * (-lmbd).exp() /

    // }

    println!("L(1)={}", subs(&Lx, 1.0));
    println!("l(1)={}", subs(&lx, 1.0));
    println!("L'(1)={}", L1);
}
