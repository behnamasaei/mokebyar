using Volo.Abp.Modularity;

namespace MokebyarCore;

[DependsOn(
    typeof(MokebyarCoreDomainModule),
    typeof(MokebyarCoreTestBaseModule)
)]
public class MokebyarCoreDomainTestModule : AbpModule
{

}
