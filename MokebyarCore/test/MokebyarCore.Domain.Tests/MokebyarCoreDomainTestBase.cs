using Volo.Abp.Modularity;

namespace MokebyarCore;

/* Inherit from this class for your domain layer tests. */
public abstract class MokebyarCoreDomainTestBase<TStartupModule> : MokebyarCoreTestBase<TStartupModule>
    where TStartupModule : IAbpModule
{

}
