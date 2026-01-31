using System.Threading.Tasks;
using Volo.Abp.DependencyInjection;

namespace MokebyarCore.Data;

/* This is used if database provider does't define
 * IMokebyarCoreDbSchemaMigrator implementation.
 */
public class NullMokebyarCoreDbSchemaMigrator : IMokebyarCoreDbSchemaMigrator, ITransientDependency
{
    public Task MigrateAsync()
    {
        return Task.CompletedTask;
    }
}
