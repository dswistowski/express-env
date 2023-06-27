FOO=$(vault read --field=value secret/some-path/foo)
export FOO
BAR=$(vault read --field=value secret/some-path/bar)
export BAR
