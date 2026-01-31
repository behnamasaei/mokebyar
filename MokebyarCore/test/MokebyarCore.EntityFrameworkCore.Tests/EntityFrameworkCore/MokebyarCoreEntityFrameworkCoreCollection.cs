using Xunit;

namespace MokebyarCore.EntityFrameworkCore;

[CollectionDefinition(MokebyarCoreTestConsts.CollectionDefinitionName)]
public class MokebyarCoreEntityFrameworkCoreCollection : ICollectionFixture<MokebyarCoreEntityFrameworkCoreFixture>
{

}
