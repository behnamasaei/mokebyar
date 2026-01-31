using MokebyarCore.EntityFrameworkCore;
using Volo.Abp.Autofac;
using Volo.Abp.Modularity;

namespace MokebyarCore.DbMigrator;

[DependsOn(
    typeof(AbpAutofacModule),
    typeof(MokebyarCoreEntityFrameworkCoreModule),
    typeof(MokebyarCoreApplicationContractsModule)
)]
public class MokebyarCoreDbMigratorModule : AbpModule
{
}
