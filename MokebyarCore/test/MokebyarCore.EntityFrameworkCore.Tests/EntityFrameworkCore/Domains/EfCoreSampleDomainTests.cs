using MokebyarCore.Samples;
using Xunit;

namespace MokebyarCore.EntityFrameworkCore.Domains;

[Collection(MokebyarCoreTestConsts.CollectionDefinitionName)]
public class EfCoreSampleDomainTests : SampleDomainTests<MokebyarCoreEntityFrameworkCoreTestModule>
{

}
