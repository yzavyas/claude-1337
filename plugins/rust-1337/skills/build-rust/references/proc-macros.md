# Procedural Macros

syn, quote, and macro development patterns.

## When to Use What

| Need | Approach |
|------|----------|
| Simple patterns | `macro_rules!` (faster compile) |
| Derive with attributes | darling + `proc_macro_derive` |
| Complex transformation | attribute macro + manual syn |
| Custom DSL | function-like proc macro |

**darling vs manual syn**: Use darling for standard attribute syntax (automatic "did you mean" suggestions). Use manual parsing for custom syntax.

## Essential Stack

**Minimal**:

```toml
[dependencies]
syn = { version = "2.0", features = ["derive"] }
quote = "1.0"
proc-macro2 = "1.0"
```

**Full**:

```toml
[dependencies]
syn = { version = "2.0", features = ["full", "parsing", "printing"] }
darling = "0.20"
proc-macro-error2 = "2.0"
```

**Testing**:

```toml
[dev-dependencies]
trybuild = "1.0"  # Compile-fail tests
```

Debug with `cargo expand`.

## Hygiene Rules

**Always use absolute paths in `quote!`**:

```rust
// Bad - may conflict with user's imports
quote! {
    Option::Some(#value)
}

// Good - unambiguous
quote! {
    ::std::option::Option::Some(#value)
}
```

## Generics Handling

```rust
fn impl_my_trait(ast: &DeriveInput) -> TokenStream {
    let name = &ast.ident;
    let generics = &ast.generics;
    let (impl_generics, ty_generics, where_clause) = generics.split_for_impl();

    quote! {
        impl #impl_generics MyTrait for #name #ty_generics #where_clause {
            fn do_thing(&self) {
                // ...
            }
        }
    }
}
```

## Error Reporting

**Use `quote_spanned!` for location**:

```rust
use syn::spanned::Spanned;

if field.ty != expected {
    return quote_spanned! {field.span()=>
        compile_error!("Field must be u32")
    };
}
```

**Span propagation**: Errors point to user's code, not macro internals.

## Compile Time Optimization

Proc macros are **11-40% of incremental build time**.

**Minimize syn features**:

```toml
# Only what you need
syn = { version = "2.0", features = ["derive"] }
# NOT features = ["full"]
```

**Optimize macro crate in dev**:

```toml
[profile.dev.build-override]
opt-level = 3
```

## Critical Gotchas

| Issue | Solution |
|-------|----------|
| Must be separate crate | `proc-macro = true` in Cargo.toml |
| Entry returns wrong type | `proc_macro::TokenStream`, not `proc_macro2` |
| Macros not exported | All macros must be in lib.rs root |
| syn 1.x → 2.x migration | `AttributeArgs` removed, lifetime changes |
| cfg in generated code | Generate the cfg, don't execute in macro |

**Crate setup**:

```toml
[package]
name = "my-macros"

[lib]
proc-macro = true

[dependencies]
syn = { version = "2.0", features = ["derive"] }
quote = "1.0"
proc-macro2 = "1.0"
```

**Basic derive macro**:

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput};

#[proc_macro_derive(MyTrait)]
pub fn derive_my_trait(input: TokenStream) -> TokenStream {
    let ast = parse_macro_input!(input as DeriveInput);
    let name = &ast.ident;

    let expanded = quote! {
        impl MyTrait for #name {
            fn name(&self) -> &'static str {
                stringify!(#name)
            }
        }
    };

    TokenStream::from(expanded)
}
```
