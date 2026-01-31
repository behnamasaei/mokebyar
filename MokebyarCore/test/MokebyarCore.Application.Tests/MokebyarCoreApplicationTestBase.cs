using Volo.Abp.Modularity;

namespace MokebyarCore;

public abstract class MokebyarCoreApplicationTestBase<TStartupModule> : MokebyarCoreTestBase<TStartupModule>
    where TStartupModule : IAbpModule
{

}
