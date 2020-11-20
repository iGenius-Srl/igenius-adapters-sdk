# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
For further informations about change log please go [here](http://keepachangelog.com/en/1.0.0/)

{{ if .Versions -}}
## [Unreleased]({{ .Info.RepositoryURL }}/compare/{{ $latest := index .Versions 0 }}{{ $latest.Tag.Name }}...master)
{{ if .Unreleased.CommitGroups -}}
{{ range .Unreleased.CommitGroups -}}
### {{ .Title }}
{{ range .Commits -}}
* {{ .Subject }} {{ if .Scope }}([{{ .Scope }}](https://igenius.atlassian.net/browse/{{ .Scope }})){{ end }}
{{ end }}
{{ end -}}
{{ end -}}
{{ end -}}

{{ range .Versions }}
## {{ if .Tag.Previous }}[{{ .Tag.Name }}]({{ $.Info.RepositoryURL }}/compare/{{ .Tag.Previous.Name }}...{{ .Tag.Name }}){{ else }}[{{ .Tag.Name }}]{{ end }} - {{ datetime "2006-01-02" .Tag.Date }}
{{ range .CommitGroups -}}
### {{ .Title }}
{{ range .Commits -}}
* {{ .Subject }} {{ if .Scope }}([{{ .Scope }}](https://igenius.atlassian.net/browse/{{ .Scope }})){{ end }}
{{ end }}
{{ end -}}
{{ end -}}
