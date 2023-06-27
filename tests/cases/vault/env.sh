FOO=$(vault read --field value secret/some-path/foo)
BAR=$(vault read --field value secret/some-path/bar)

export FOO
export BAR
