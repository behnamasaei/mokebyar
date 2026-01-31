using System.Threading.Tasks;

namespace MokebyarCore.Data;

public interface IMokebyarCoreDbSchemaMigrator
{
    Task MigrateAsync();
}
