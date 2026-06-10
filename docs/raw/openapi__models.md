https://fastapi.tiangolo.com/reference/openapi/models/
# OpenAPI `models`[¶](#openapi-models "Permanent link")

OpenAPI Pydantic models used to generate and validate the generated OpenAPI.

## fastapi.openapi.models [¶](#fastapi.openapi.models "Permanent link")

### SchemaType `module-attribute` [¶](#fastapi.openapi.models.SchemaType "Permanent link")

```python
SchemaType = Literal[
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
]
```

### SchemaOrBool `module-attribute` [¶](#fastapi.openapi.models.SchemaOrBool "Permanent link")

```python
SchemaOrBool = Schema | bool
```

### SecurityScheme `module-attribute` [¶](#fastapi.openapi.models.SecurityScheme "Permanent link")

```python
SecurityScheme = (
    APIKey | HTTPBase | OAuth2 | OpenIdConnect | HTTPBearer
)
```

### BaseModelWithConfig [¶](#fastapi.openapi.models.BaseModelWithConfig "Permanent link")

Bases: `BaseModel`

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.BaseModelWithConfig.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Contact [¶](#fastapi.openapi.models.Contact "Permanent link")

Bases: `BaseModelWithConfig`

#### name `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Contact.name "Permanent link")

```python
name = None
```

#### url `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Contact.url "Permanent link")

```python
url = None
```

#### email `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Contact.email "Permanent link")

```python
email = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Contact.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### License [¶](#fastapi.openapi.models.License "Permanent link")

Bases: `BaseModelWithConfig`

#### name `instance-attribute` [¶](#fastapi.openapi.models.License.name "Permanent link")

```python
name
```

#### identifier `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.License.identifier "Permanent link")

```python
identifier = None
```

#### url `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.License.url "Permanent link")

```python
url = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.License.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Info [¶](#fastapi.openapi.models.Info "Permanent link")

Bases: `BaseModelWithConfig`

#### title `instance-attribute` [¶](#fastapi.openapi.models.Info.title "Permanent link")

```python
title
```

#### summary `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.summary "Permanent link")

```python
summary = None
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.description "Permanent link")

```python
description = None
```

#### termsOfService `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.termsOfService "Permanent link")

```python
termsOfService = None
```

#### contact `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.contact "Permanent link")

```python
contact = None
```

#### license `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.license "Permanent link")

```python
license = None
```

#### version `instance-attribute` [¶](#fastapi.openapi.models.Info.version "Permanent link")

```python
version
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Info.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### ServerVariable [¶](#fastapi.openapi.models.ServerVariable "Permanent link")

Bases: `BaseModelWithConfig`

#### enum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ServerVariable.enum "Permanent link")

```python
enum = None
```

#### default `instance-attribute` [¶](#fastapi.openapi.models.ServerVariable.default "Permanent link")

```python
default
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ServerVariable.description "Permanent link")

```python
description = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ServerVariable.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Server [¶](#fastapi.openapi.models.Server "Permanent link")

Bases: `BaseModelWithConfig`

#### url `instance-attribute` [¶](#fastapi.openapi.models.Server.url "Permanent link")

```python
url
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Server.description "Permanent link")

```python
description = None
```

#### variables `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Server.variables "Permanent link")

```python
variables = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Server.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Reference [¶](#fastapi.openapi.models.Reference "Permanent link")

Bases: `BaseModel`

#### ref `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Reference.ref "Permanent link")

```python
ref = Field(alias='$ref')
```

### Discriminator [¶](#fastapi.openapi.models.Discriminator "Permanent link")

Bases: `BaseModel`

#### propertyName `instance-attribute` [¶](#fastapi.openapi.models.Discriminator.propertyName "Permanent link")

```python
propertyName
```

#### mapping `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Discriminator.mapping "Permanent link")

```python
mapping = None
```

### XML [¶](#fastapi.openapi.models.XML "Permanent link")

Bases: `BaseModelWithConfig`

#### name `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.name "Permanent link")

```python
name = None
```

#### namespace `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.namespace "Permanent link")

```python
namespace = None
```

#### prefix `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.prefix "Permanent link")

```python
prefix = None
```

#### attribute `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.attribute "Permanent link")

```python
attribute = None
```

#### wrapped `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.wrapped "Permanent link")

```python
wrapped = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.XML.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### ExternalDocumentation [¶](#fastapi.openapi.models.ExternalDocumentation "Permanent link")

Bases: `BaseModelWithConfig`

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ExternalDocumentation.description "Permanent link")

```python
description = None
```

#### url `instance-attribute` [¶](#fastapi.openapi.models.ExternalDocumentation.url "Permanent link")

```python
url
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ExternalDocumentation.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Schema [¶](#fastapi.openapi.models.Schema "Permanent link")

Bases: `BaseModelWithConfig`

#### schema\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.schema_ "Permanent link")

```python
schema_ = Field(default=None, alias='$schema')
```

#### vocabulary `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.vocabulary "Permanent link")

```python
vocabulary = Field(default=None, alias='$vocabulary')
```

#### id `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.id "Permanent link")

```python
id = Field(default=None, alias='$id')
```

#### anchor `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.anchor "Permanent link")

```python
anchor = Field(default=None, alias='$anchor')
```

#### dynamicAnchor `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.dynamicAnchor "Permanent link")

```python
dynamicAnchor = Field(default=None, alias='$dynamicAnchor')
```

#### ref `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.ref "Permanent link")

```python
ref = Field(default=None, alias='$ref')
```

#### dynamicRef `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.dynamicRef "Permanent link")

```python
dynamicRef = Field(default=None, alias='$dynamicRef')
```

#### defs `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.defs "Permanent link")

```python
defs = Field(default=None, alias='$defs')
```

#### comment `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.comment "Permanent link")

```python
comment = Field(default=None, alias='$comment')
```

#### allOf `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.allOf "Permanent link")

```python
allOf = None
```

#### anyOf `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.anyOf "Permanent link")

```python
anyOf = None
```

#### oneOf `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.oneOf "Permanent link")

```python
oneOf = None
```

#### not\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.not_ "Permanent link")

```python
not_ = Field(default=None, alias='not')
```

#### if\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.if_ "Permanent link")

```python
if_ = Field(default=None, alias='if')
```

#### then `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.then "Permanent link")

```python
then = None
```

#### else\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.else_ "Permanent link")

```python
else_ = Field(default=None, alias='else')
```

#### dependentSchemas `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.dependentSchemas "Permanent link")

```python
dependentSchemas = None
```

#### prefixItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.prefixItems "Permanent link")

```python
prefixItems = None
```

#### items `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.items "Permanent link")

```python
items = None
```

#### contains `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.contains "Permanent link")

```python
contains = None
```

#### properties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.properties "Permanent link")

```python
properties = None
```

#### patternProperties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.patternProperties "Permanent link")

```python
patternProperties = None
```

#### additionalProperties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.additionalProperties "Permanent link")

```python
additionalProperties = None
```

#### propertyNames `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.propertyNames "Permanent link")

```python
propertyNames = None
```

#### unevaluatedItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.unevaluatedItems "Permanent link")

```python
unevaluatedItems = None
```

#### unevaluatedProperties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.unevaluatedProperties "Permanent link")

```python
unevaluatedProperties = None
```

#### type `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.type "Permanent link")

```python
type = None
```

#### enum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.enum "Permanent link")

```python
enum = None
```

#### const `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.const "Permanent link")

```python
const = None
```

#### multipleOf `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.multipleOf "Permanent link")

```python
multipleOf = Field(default=None, gt=0)
```

#### maximum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.maximum "Permanent link")

```python
maximum = None
```

#### exclusiveMaximum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.exclusiveMaximum "Permanent link")

```python
exclusiveMaximum = None
```

#### minimum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.minimum "Permanent link")

```python
minimum = None
```

#### exclusiveMinimum `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.exclusiveMinimum "Permanent link")

```python
exclusiveMinimum = None
```

#### maxLength `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.maxLength "Permanent link")

```python
maxLength = Field(default=None, ge=0)
```

#### minLength `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.minLength "Permanent link")

```python
minLength = Field(default=None, ge=0)
```

#### pattern `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.pattern "Permanent link")

```python
pattern = None
```

#### maxItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.maxItems "Permanent link")

```python
maxItems = Field(default=None, ge=0)
```

#### minItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.minItems "Permanent link")

```python
minItems = Field(default=None, ge=0)
```

#### uniqueItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.uniqueItems "Permanent link")

```python
uniqueItems = None
```

#### maxContains `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.maxContains "Permanent link")

```python
maxContains = Field(default=None, ge=0)
```

#### minContains `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.minContains "Permanent link")

```python
minContains = Field(default=None, ge=0)
```

#### maxProperties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.maxProperties "Permanent link")

```python
maxProperties = Field(default=None, ge=0)
```

#### minProperties `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.minProperties "Permanent link")

```python
minProperties = Field(default=None, ge=0)
```

#### required `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.required "Permanent link")

```python
required = None
```

#### dependentRequired `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.dependentRequired "Permanent link")

```python
dependentRequired = None
```

#### format `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.format "Permanent link")

```python
format = None
```

#### contentEncoding `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.contentEncoding "Permanent link")

```python
contentEncoding = None
```

#### contentMediaType `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.contentMediaType "Permanent link")

```python
contentMediaType = None
```

#### contentSchema `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.contentSchema "Permanent link")

```python
contentSchema = None
```

#### title `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.title "Permanent link")

```python
title = None
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.description "Permanent link")

```python
description = None
```

#### default `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.default "Permanent link")

```python
default = None
```

#### deprecated `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.deprecated "Permanent link")

```python
deprecated = None
```

#### readOnly `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.readOnly "Permanent link")

```python
readOnly = None
```

#### writeOnly `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.writeOnly "Permanent link")

```python
writeOnly = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.examples "Permanent link")

```python
examples = None
```

#### discriminator `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.discriminator "Permanent link")

```python
discriminator = None
```

#### xml `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.xml "Permanent link")

```python
xml = None
```

#### externalDocs `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.externalDocs "Permanent link")

```python
externalDocs = None
```

#### example `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.example "Permanent link")

```python
example = None
```

Deprecated in OpenAPI 3.1.0 that now uses JSON Schema 2020-12, although still supported. Use examples instead.

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Schema.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Example [¶](#fastapi.openapi.models.Example "Permanent link")

Bases: `TypedDict`

#### summary `instance-attribute` [¶](#fastapi.openapi.models.Example.summary "Permanent link")

```python
summary
```

#### description `instance-attribute` [¶](#fastapi.openapi.models.Example.description "Permanent link")

```python
description
```

#### value `instance-attribute` [¶](#fastapi.openapi.models.Example.value "Permanent link")

```python
value
```

#### externalValue `instance-attribute` [¶](#fastapi.openapi.models.Example.externalValue "Permanent link")

```python
externalValue
```

### ParameterInType [¶](#fastapi.openapi.models.ParameterInType "Permanent link")

Bases: `Enum`

#### query `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterInType.query "Permanent link")

```python
query = 'query'
```

#### header `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterInType.header "Permanent link")

```python
header = 'header'
```

#### path `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterInType.path "Permanent link")

```python
path = 'path'
```

#### cookie `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterInType.cookie "Permanent link")

```python
cookie = 'cookie'
```

### Encoding [¶](#fastapi.openapi.models.Encoding "Permanent link")

Bases: `BaseModelWithConfig`

#### contentType `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.contentType "Permanent link")

```python
contentType = None
```

#### headers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.headers "Permanent link")

```python
headers = None
```

#### style `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.style "Permanent link")

```python
style = None
```

#### explode `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.explode "Permanent link")

```python
explode = None
```

#### allowReserved `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.allowReserved "Permanent link")

```python
allowReserved = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Encoding.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### MediaType [¶](#fastapi.openapi.models.MediaType "Permanent link")

Bases: `BaseModelWithConfig`

#### schema\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.MediaType.schema_ "Permanent link")

```python
schema_ = Field(default=None, alias='schema')
```

#### example `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.MediaType.example "Permanent link")

```python
example = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.MediaType.examples "Permanent link")

```python
examples = None
```

#### encoding `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.MediaType.encoding "Permanent link")

```python
encoding = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.MediaType.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### ParameterBase [¶](#fastapi.openapi.models.ParameterBase "Permanent link")

Bases: `BaseModelWithConfig`

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.description "Permanent link")

```python
description = None
```

#### required `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.required "Permanent link")

```python
required = None
```

#### deprecated `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.deprecated "Permanent link")

```python
deprecated = None
```

#### style `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.style "Permanent link")

```python
style = None
```

#### explode `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.explode "Permanent link")

```python
explode = None
```

#### allowReserved `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.allowReserved "Permanent link")

```python
allowReserved = None
```

#### schema\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.schema_ "Permanent link")

```python
schema_ = Field(default=None, alias='schema')
```

#### example `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.example "Permanent link")

```python
example = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.examples "Permanent link")

```python
examples = None
```

#### content `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.content "Permanent link")

```python
content = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.ParameterBase.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Parameter [¶](#fastapi.openapi.models.Parameter "Permanent link")

Bases: `ParameterBase`

#### name `instance-attribute` [¶](#fastapi.openapi.models.Parameter.name "Permanent link")

```python
name
```

#### in\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.in_ "Permanent link")

```python
in_ = Field(alias='in')
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.description "Permanent link")

```python
description = None
```

#### required `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.required "Permanent link")

```python
required = None
```

#### deprecated `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.deprecated "Permanent link")

```python
deprecated = None
```

#### style `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.style "Permanent link")

```python
style = None
```

#### explode `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.explode "Permanent link")

```python
explode = None
```

#### allowReserved `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.allowReserved "Permanent link")

```python
allowReserved = None
```

#### schema\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.schema_ "Permanent link")

```python
schema_ = Field(default=None, alias='schema')
```

#### example `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.example "Permanent link")

```python
example = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.examples "Permanent link")

```python
examples = None
```

#### content `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Parameter.content "Permanent link")

```python
content = None
```

### Header [¶](#fastapi.openapi.models.Header "Permanent link")

Bases: `ParameterBase`

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.description "Permanent link")

```python
description = None
```

#### required `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.required "Permanent link")

```python
required = None
```

#### deprecated `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.deprecated "Permanent link")

```python
deprecated = None
```

#### style `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.style "Permanent link")

```python
style = None
```

#### explode `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.explode "Permanent link")

```python
explode = None
```

#### allowReserved `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.allowReserved "Permanent link")

```python
allowReserved = None
```

#### schema\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.schema_ "Permanent link")

```python
schema_ = Field(default=None, alias='schema')
```

#### example `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.example "Permanent link")

```python
example = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.examples "Permanent link")

```python
examples = None
```

#### content `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Header.content "Permanent link")

```python
content = None
```

### RequestBody [¶](#fastapi.openapi.models.RequestBody "Permanent link")

Bases: `BaseModelWithConfig`

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.RequestBody.description "Permanent link")

```python
description = None
```

#### content `instance-attribute` [¶](#fastapi.openapi.models.RequestBody.content "Permanent link")

```python
content
```

#### required `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.RequestBody.required "Permanent link")

```python
required = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.RequestBody.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Link [¶](#fastapi.openapi.models.Link "Permanent link")

Bases: `BaseModelWithConfig`

#### operationRef `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.operationRef "Permanent link")

```python
operationRef = None
```

#### operationId `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.operationId "Permanent link")

```python
operationId = None
```

#### parameters `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.parameters "Permanent link")

```python
parameters = None
```

#### requestBody `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.requestBody "Permanent link")

```python
requestBody = None
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.description "Permanent link")

```python
description = None
```

#### server `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.server "Permanent link")

```python
server = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Link.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Response [¶](#fastapi.openapi.models.Response "Permanent link")

Bases: `BaseModelWithConfig`

#### description `instance-attribute` [¶](#fastapi.openapi.models.Response.description "Permanent link")

```python
description
```

#### headers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Response.headers "Permanent link")

```python
headers = None
```

#### content `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Response.content "Permanent link")

```python
content = None
```

#### links `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Response.links "Permanent link")

```python
links = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Response.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Operation [¶](#fastapi.openapi.models.Operation "Permanent link")

Bases: `BaseModelWithConfig`

#### tags `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.tags "Permanent link")

```python
tags = None
```

#### summary `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.summary "Permanent link")

```python
summary = None
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.description "Permanent link")

```python
description = None
```

#### externalDocs `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.externalDocs "Permanent link")

```python
externalDocs = None
```

#### operationId `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.operationId "Permanent link")

```python
operationId = None
```

#### parameters `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.parameters "Permanent link")

```python
parameters = None
```

#### requestBody `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.requestBody "Permanent link")

```python
requestBody = None
```

#### responses `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.responses "Permanent link")

```python
responses = None
```

#### callbacks `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.callbacks "Permanent link")

```python
callbacks = None
```

#### deprecated `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.deprecated "Permanent link")

```python
deprecated = None
```

#### security `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.security "Permanent link")

```python
security = None
```

#### servers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.servers "Permanent link")

```python
servers = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Operation.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### PathItem [¶](#fastapi.openapi.models.PathItem "Permanent link")

Bases: `BaseModelWithConfig`

#### ref `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.ref "Permanent link")

```python
ref = Field(default=None, alias='$ref')
```

#### summary `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.summary "Permanent link")

```python
summary = None
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.description "Permanent link")

```python
description = None
```

#### get `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.get "Permanent link")

```python
get = None
```

#### put `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.put "Permanent link")

```python
put = None
```

#### post `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.post "Permanent link")

```python
post = None
```

#### delete `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.delete "Permanent link")

```python
delete = None
```

#### options `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.options "Permanent link")

```python
options = None
```

#### head `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.head "Permanent link")

```python
head = None
```

#### patch `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.patch "Permanent link")

```python
patch = None
```

#### trace `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.trace "Permanent link")

```python
trace = None
```

#### servers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.servers "Permanent link")

```python
servers = None
```

#### parameters `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.parameters "Permanent link")

```python
parameters = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.PathItem.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### SecuritySchemeType [¶](#fastapi.openapi.models.SecuritySchemeType "Permanent link")

Bases: `Enum`

#### apiKey `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecuritySchemeType.apiKey "Permanent link")

```python
apiKey = 'apiKey'
```

#### http `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecuritySchemeType.http "Permanent link")

```python
http = 'http'
```

#### oauth2 `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecuritySchemeType.oauth2 "Permanent link")

```python
oauth2 = 'oauth2'
```

#### openIdConnect `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecuritySchemeType.openIdConnect "Permanent link")

```python
openIdConnect = 'openIdConnect'
```

### SecurityBase [¶](#fastapi.openapi.models.SecurityBase "Permanent link")

Bases: `BaseModelWithConfig`

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecurityBase.type_ "Permanent link")

```python
type_ = Field(alias='type')
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecurityBase.description "Permanent link")

```python
description = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.SecurityBase.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### APIKeyIn [¶](#fastapi.openapi.models.APIKeyIn "Permanent link")

Bases: `Enum`

#### query `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKeyIn.query "Permanent link")

```python
query = 'query'
```

#### header `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKeyIn.header "Permanent link")

```python
header = 'header'
```

#### cookie `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKeyIn.cookie "Permanent link")

```python
cookie = 'cookie'
```

### APIKey [¶](#fastapi.openapi.models.APIKey "Permanent link")

Bases: `SecurityBase`

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKey.type_ "Permanent link")

```python
type_ = Field(default=apiKey, alias='type')
```

#### in\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKey.in_ "Permanent link")

```python
in_ = Field(alias='in')
```

#### name `instance-attribute` [¶](#fastapi.openapi.models.APIKey.name "Permanent link")

```python
name
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKey.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.APIKey.description "Permanent link")

```python
description = None
```

### HTTPBase [¶](#fastapi.openapi.models.HTTPBase "Permanent link")

Bases: `SecurityBase`

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBase.type_ "Permanent link")

```python
type_ = Field(default=http, alias='type')
```

#### scheme `instance-attribute` [¶](#fastapi.openapi.models.HTTPBase.scheme "Permanent link")

```python
scheme
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBase.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBase.description "Permanent link")

```python
description = None
```

### HTTPBearer [¶](#fastapi.openapi.models.HTTPBearer "Permanent link")

Bases: `HTTPBase`

#### scheme `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBearer.scheme "Permanent link")

```python
scheme = 'bearer'
```

#### bearerFormat `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBearer.bearerFormat "Permanent link")

```python
bearerFormat = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBearer.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBearer.type_ "Permanent link")

```python
type_ = Field(default=http, alias='type')
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.HTTPBearer.description "Permanent link")

```python
description = None
```

### OAuthFlow [¶](#fastapi.openapi.models.OAuthFlow "Permanent link")

Bases: `BaseModelWithConfig`

#### refreshUrl `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlow.refreshUrl "Permanent link")

```python
refreshUrl = None
```

#### scopes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlow.scopes "Permanent link")

```python
scopes = {}
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlow.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### OAuthFlowImplicit [¶](#fastapi.openapi.models.OAuthFlowImplicit "Permanent link")

Bases: `OAuthFlow`

#### authorizationUrl `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowImplicit.authorizationUrl "Permanent link")

```python
authorizationUrl
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowImplicit.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### refreshUrl `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowImplicit.refreshUrl "Permanent link")

```python
refreshUrl = None
```

#### scopes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowImplicit.scopes "Permanent link")

```python
scopes = {}
```

### OAuthFlowPassword [¶](#fastapi.openapi.models.OAuthFlowPassword "Permanent link")

Bases: `OAuthFlow`

#### tokenUrl `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowPassword.tokenUrl "Permanent link")

```python
tokenUrl
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowPassword.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### refreshUrl `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowPassword.refreshUrl "Permanent link")

```python
refreshUrl = None
```

#### scopes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowPassword.scopes "Permanent link")

```python
scopes = {}
```

### OAuthFlowClientCredentials [¶](#fastapi.openapi.models.OAuthFlowClientCredentials "Permanent link")

Bases: `OAuthFlow`

#### tokenUrl `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowClientCredentials.tokenUrl "Permanent link")

```python
tokenUrl
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowClientCredentials.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### refreshUrl `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowClientCredentials.refreshUrl "Permanent link")

```python
refreshUrl = None
```

#### scopes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowClientCredentials.scopes "Permanent link")

```python
scopes = {}
```

### OAuthFlowAuthorizationCode [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode "Permanent link")

Bases: `OAuthFlow`

#### authorizationUrl `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode.authorizationUrl "Permanent link")

```python
authorizationUrl
```

#### tokenUrl `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode.tokenUrl "Permanent link")

```python
tokenUrl
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### refreshUrl `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode.refreshUrl "Permanent link")

```python
refreshUrl = None
```

#### scopes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlowAuthorizationCode.scopes "Permanent link")

```python
scopes = {}
```

### OAuthFlows [¶](#fastapi.openapi.models.OAuthFlows "Permanent link")

Bases: `BaseModelWithConfig`

#### implicit `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlows.implicit "Permanent link")

```python
implicit = None
```

#### password `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlows.password "Permanent link")

```python
password = None
```

#### clientCredentials `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlows.clientCredentials "Permanent link")

```python
clientCredentials = None
```

#### authorizationCode `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlows.authorizationCode "Permanent link")

```python
authorizationCode = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuthFlows.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### OAuth2 [¶](#fastapi.openapi.models.OAuth2 "Permanent link")

Bases: `SecurityBase`

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuth2.type_ "Permanent link")

```python
type_ = Field(default=oauth2, alias='type')
```

#### flows `instance-attribute` [¶](#fastapi.openapi.models.OAuth2.flows "Permanent link")

```python
flows
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuth2.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OAuth2.description "Permanent link")

```python
description = None
```

### OpenIdConnect [¶](#fastapi.openapi.models.OpenIdConnect "Permanent link")

Bases: `SecurityBase`

#### type\_ `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenIdConnect.type_ "Permanent link")

```python
type_ = Field(default=openIdConnect, alias='type')
```

#### openIdConnectUrl `instance-attribute` [¶](#fastapi.openapi.models.OpenIdConnect.openIdConnectUrl "Permanent link")

```python
openIdConnectUrl
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenIdConnect.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenIdConnect.description "Permanent link")

```python
description = None
```

### Components [¶](#fastapi.openapi.models.Components "Permanent link")

Bases: `BaseModelWithConfig`

#### schemas `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.schemas "Permanent link")

```python
schemas = None
```

#### responses `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.responses "Permanent link")

```python
responses = None
```

#### parameters `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.parameters "Permanent link")

```python
parameters = None
```

#### examples `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.examples "Permanent link")

```python
examples = None
```

#### requestBodies `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.requestBodies "Permanent link")

```python
requestBodies = None
```

#### headers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.headers "Permanent link")

```python
headers = None
```

#### securitySchemes `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.securitySchemes "Permanent link")

```python
securitySchemes = None
```

#### links `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.links "Permanent link")

```python
links = None
```

#### callbacks `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.callbacks "Permanent link")

```python
callbacks = None
```

#### pathItems `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.pathItems "Permanent link")

```python
pathItems = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Components.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### Tag [¶](#fastapi.openapi.models.Tag "Permanent link")

Bases: `BaseModelWithConfig`

#### name `instance-attribute` [¶](#fastapi.openapi.models.Tag.name "Permanent link")

```python
name
```

#### description `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Tag.description "Permanent link")

```python
description = None
```

#### externalDocs `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Tag.externalDocs "Permanent link")

```python
externalDocs = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.Tag.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```

### OpenAPI [¶](#fastapi.openapi.models.OpenAPI "Permanent link")

Bases: `BaseModelWithConfig`

#### openapi `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.openapi "Permanent link")

```python
openapi
```

#### info `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.info "Permanent link")

```python
info
```

#### jsonSchemaDialect `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.jsonSchemaDialect "Permanent link")

```python
jsonSchemaDialect = None
```

#### servers `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.servers "Permanent link")

```python
servers = None
```

#### paths `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.paths "Permanent link")

```python
paths = None
```

#### webhooks `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.webhooks "Permanent link")

```python
webhooks = None
```

#### components `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.components "Permanent link")

```python
components = None
```

#### security `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.security "Permanent link")

```python
security = None
```

#### tags `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.tags "Permanent link")

```python
tags = None
```

#### externalDocs `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.externalDocs "Permanent link")

```python
externalDocs = None
```

#### model\_config `class-attribute` `instance-attribute` [¶](#fastapi.openapi.models.OpenAPI.model_config "Permanent link")

```python
model_config = {'extra': 'allow'}
```
