using Volo.Abp.Modularity;

namespace MokebyarCore;

[DependsOn(
    typeof(MokebyarCoreApplicationModule),
    typeof(MokebyarCoreDomainTestModule)
)]
public class MokebyarCoreApplicationTestModule : AbpModule
{

}
