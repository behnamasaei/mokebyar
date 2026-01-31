using MokebyarCore.Samples;
using Xunit;

namespace MokebyarCore.EntityFrameworkCore.Applications;

[Collection(MokebyarCoreTestConsts.CollectionDefinitionName)]
public class EfCoreSampleAppServiceTests : SampleAppServiceTests<MokebyarCoreEntityFrameworkCoreTestModule>
{

}
